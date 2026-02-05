#!/bin/bash

# Restart the lldpd service
sudo service lldpd restart

# Loop until the contents of neighbors.txt are received
while true; do
    # Run the lldpctl command and capture the output
    interface="eth0" # "enp0s13f0u2u2"
    output=$(sudo lldpctl "$interface")

    # Check if the output contains the expected lines
    if echo "$output" | grep -q "SysName:" && echo "$output" | grep -q "PortID:" && echo "$output" | grep -q "PortDescr:"; then
        # Output the required lines
        echo "$output" | grep "SysName:" | sed 's/^[[:space:]]*//'
        echo "$output" | grep "PortID:" | sed 's/^[[:space:]]*//'
        echo "$output" | grep "PortDescr:" | sed 's/^[[:space:]]*//'
        echo "$output" | grep "VLAN:" | sed 's/^[[:space:]]*//'
        break
    fi
    # Sleep for a short duration before the next iteration
    sleep 2
done
# Append captured data to log file with timestamp
{
    echo "$(date '+%Y-%m-%d %H:%M:%S')"
    echo "$output"
    echo "---"
} >> ~/lldp_log.txt
# Stop the lldpd service
sudo service lldpd stop