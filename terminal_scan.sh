#!/bin/bash
set -u

MAX_RETRIES=30
SLEEP_SECONDS=2
LOG_FILE="$HOME/lldp_log.txt"
STOP_LLDPD_ON_EXIT=0   # set to 1 only if you want to stop daemon at end

# Verify required commands exist
for cmd in ip awk cut grep sed date sudo systemctl lldpctl; do
    command -v "$cmd" >/dev/null 2>&1 || {
        echo "Missing required command: $cmd"
        exit 1
    }
done

# Ensure lldpd is running (creates /run/lldpd.socket)
if ! systemctl is-active --quiet lldpd; then
    echo "Starting lldpd service..."
    sudo systemctl start lldpd || {
        echo "Failed to start lldpd. Check: sudo systemctl status lldpd"
        exit 1
    }
fi

mapfile -t interfaces < <(ip -o link show | awk -F': ' '$2 != "lo" {print $2}' | cut -d'@' -f1)

if [ ${#interfaces[@]} -eq 0 ]; then
    echo "No network interfaces found."
    exit 1
fi

echo "Available network interfaces:"
select interface in "${interfaces[@]}"; do
    if [ -n "${interface:-}" ]; then
        break
    fi
    echo "Invalid selection. Try again."
done

output=""
for ((i=1; i<=MAX_RETRIES; i++)); do
    output=$(sudo lldpctl "$interface" 2>&1 || true)

    if echo "$output" | grep -q "SysName:" \
       && echo "$output" | grep -q "PortID:" \
       && echo "$output" | grep -q "PortDescr:"; then
        echo "$output" | grep "SysName:"   | sed 's/^[[:space:]]*//'
        echo "$output" | grep "PortID:"    | sed 's/^[[:space:]]*//'
        echo "$output" | grep "PortDescr:" | sed 's/^[[:space:]]*//'
        echo "$output" | grep "VLAN:"      | sed 's/^[[:space:]]*//'
        break
    fi

    if [ "$i" -eq "$MAX_RETRIES" ]; then
        echo "No LLDP neighbor data found after $MAX_RETRIES attempts."
        echo "Last lldpctl output:"
        echo "$output"
        exit 2
    fi

    sleep "$SLEEP_SECONDS"
done

# Append captured data to log file with timestamp
{
    echo "$(date '+%Y-%m-%d %H:%M:%S')"
    echo "$output"
    echo "---"
} >> "$LOG_FILE"

# Usually keep lldpd running to avoid next-run socket errors
if [ "$STOP_LLDPD_ON_EXIT" -eq 1 ]; then
    sudo systemctl stop lldpd
fi