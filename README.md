# Network Port Scanner - LLDP Neighbor Discovery

This repository contains bash scripts and utilities for discovering and managing LLDP (Link Layer Discovery Protocol) neighbors on Linux systems.

## Overview

The `netportscan` project provides tools to install, restart, and query the LLDP daemon (`lldpd`) to discover network neighbor information. This is useful for network administration, device inventory, and connectivity troubleshooting.

## Files

### Scripts

- **`install_lldpd.sh`** - Installation script for the LLDP daemon
  - Updates package manager
  - Installs lldpd service
  - Enables lldpd to start on boot
  - See [install_lldpd.sh](install_lldpd.sh) for details

- **`restart_lldpd.sh`** - Main neighbor discovery script
  - Restarts the lldpd service
  - Polls network interface for LLDP neighbor information
  - Captures system name, port ID, port description, and VLAN info
  - Logs results with timestamps to `~/lldp_log.txt`
  - See [RESTART_LLDPD_README.md](RESTART_LLDPD_README.md) for detailed documentation

- **`show_heighbours.sh`** - Display LLDP neighbors
  - Shows current LLDP neighbor information
  - Note: File name appears to have a typo ("heighbours" instead of "neighbours")

### Documentation & Samples

- **`RESTART_LLDPD_README.md`** - Comprehensive documentation for the restart_lldpd.sh script
  - Prerequisites and configuration options
  - Usage instructions
  - Troubleshooting guide

- **`neighors.txt`** - Sample neighbor information captured from LLDP
  - Example output from LLDP discovery

- **`SAMPLE LDP neighbors Interface.txt`** - Sample LLDP output
  - Reference data showing expected LLDP output format

## Quick Start

### 1. Install LLDPD (if not already installed)
```bash
bash install_lldpd.sh
```

### 2. Discover Network Neighbors
```bash
sudo bash restart_lldpd.sh
```

### 3. View Discovered Neighbors
```bash
bash show_heighbours.sh
```

## Requirements

- Linux/Unix system with bash shell
- Root or sudo privileges
- Active network interface connected to LLDP-capable devices
- `lldpd` service must be installed

## Configuration

The default network interface is `enp0s13f0u2u2`. To use a different interface, edit the script and modify the `interface` variable:

```bash
interface="your-interface-name"  # e.g., eth0, ens0, enp0s31f6
```

## Output

When you run `restart_lldpd.sh`, it captures and displays:
- **System Name** - Hostname of the neighboring device
- **Port ID** - Interface identifier on the neighboring device
- **Port Description** - Description of the port
- **VLAN Information** - Virtual LAN configuration

Results are logged to `~/lldp_log.txt` with timestamps for future reference.

## References

- [LLDPD Project](https://github.com/lldpd/lldpd)
- [LLDPD Documentation](https://lldpd.github.io/)
- [LLDP Protocol Information](https://en.wikipedia.org/wiki/Link_Layer_Discovery_Protocol)

## Notes

- The restart_lldpd.sh script requires sudo privileges
- LLDP neighbors must support LLDP for discovery to work
- The script polls the interface until neighbor data is received (with 2-second intervals)
- All output is logged with timestamps for auditing purposes

## Troubleshooting

For detailed troubleshooting information, see [RESTART_LLDPD_README.md](RESTART_LLDPD_README.md#troubleshooting).

Common issues:
- **Service not found** - Install lldpd first using `install_lldpd.sh`
- **No neighbor info** - Verify interface name and LLDP support on connected devices
- **Permission denied** - Run scripts with sudo
