#!/bin/bash
# Update package manager
sudo apt-get update

# Install lldpd
sudo apt-get install -y cdpr dia ethtool iperf lldpd speedtest-cli

# Start the lldpd service
sudo service lldpd start

# Enable lldpd to start on boot
sudo systemctl enable lldpd

sudo systemctl deamon-reload 

echo "Tools installation and setup completed successfully!"


