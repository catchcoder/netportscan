#!/bin/bash

# Go to project directory
cd /home/pi/repos/netportscan

# Start the lldpd scanning script in the background
./home/pi/repos/netportscan/scan_lldpd.sh &

# Activate the python venv
source /home/pi/netportscan/bin/activate

# Run Python script
python tui.py
