#!/bin/bash
# Update package manager
sudo apt-get update

# Install lldpd
sudo apt-get install -y lldpd

# Start the lldpd service
sudo service lldpd start

# Enable lldpd to start on boot
sudo systemctl enable lldpd

echo "lldpd installation and setup completed successfully!"
