#!/bin/bash

# Loop until the contents of neighbors.txt are received    # Run the lldpctl command and capture the output
mapfile -t interfaces < <(ip -o link show | awk -F': ' '$2 != "lo" {print $2}' | cut -d'@' -f1)

if [ ${#interfaces[@]} -eq 0 ]; then
    echo "No network interfaces found."
    exit 1
fi

echo "Available network interfaces:"
select interface in "${interfaces[@]}"; do
    if [ -n "$interface" ]; then
        break
    fi
    echo "Invalid selection. Try again."
done

sudo lldpctl "$interface"

    # Sleep for a short duration before the next iteratio

