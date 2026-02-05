#!/bin/bash

# Go to project directory
cd /home/pi/netportscan

# Start the lldpd scanning script in the background
./home/pi/netportscan/scan_lldpd.sh &

# Activate the python venv
source /home/pi/netportscan/venv/bin/activate

# Run Python script
python tui.py
