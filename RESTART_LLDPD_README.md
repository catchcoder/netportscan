# Running restart_lldpd.sh

## Overview
`restart_lldpd.sh` is a bash script that restarts the LLDP daemon (lldpd) and captures neighbor discovery information from a specific network interface. More information can be found here https://github.com/lldpd/lldpd and https://lldpd.github.io/

## Prerequisites
- Linux/Unix system with bash shell
- `lldpd` service installed and available
- `sudo` privileges (required for service restart and lldpctl commands)
- Active network interface (default: `enp0s13f0u2u2`)

## What the Script Does
1. Restarts the `lldpd` service
2. Polls the specified network interface for LLDP neighbor information
3. Extracts and displays:
   - System Name (SysName)
   - Port ID (PortID)
   - Port Description (PortDescr)
   - VLAN information
4. Logs the output to `~/lldp_log.txt` with a timestamp
5. Stops the `lldpd` service

## Usage

### Basic Execution

```bash
bash restart_lldpd.sh
```

Or make the script executable first:
```bash
chmod +x restart_lldpd.sh
./restart_lldpd.sh
```

### Running with sudo
Since the script requires sudo privileges:
```bash
sudo bash restart_lldpd.sh
```

## Configuration

### Changing the Network Interface
Edit the script and modify this line to use a different interface:
```bash
interface="enp0s13f0u2u2"
```
Replace `enp0s13f0u2u2` with your desired network interface name (e.g., `eth0`, `ens0`).

### Adjusting Poll Frequency
To change how often the script checks for neighbor data, modify:
```bash
sleep 2
```
Change `2` to your desired seconds between polling attempts.

## Output

### Console Output
The script displays the captured LLDP neighbor information:
- System Name
- Port ID
- Port Description
- VLAN Information

### Log File
Results are appended to `~/lldp_log.txt` with timestamps in the format:
```
YYYY-MM-DD HH:MM:SS
[Full lldpctl output]
---
```

## Troubleshooting

### Service Not Found
If you get "lldpd: unrecognized service", ensure lldpd is installed:
```bash
sudo apt-get install lldpd    # On Debian/Ubuntu
sudo yum install lldpd        # On CentOS/RHEL
```

### No Neighbor Information
- Verify the interface name is correct
- Ensure the interface is connected to a device that supports LLDP
- Check that LLDP is enabled on connected devices
- Wait for LLDP discovery to complete (may take a few seconds)

### Permission Denied
Run the script with sudo:
```bash
sudo bash restart_lldpd.sh
```

## Related Files
- `install_lldpd.sh` - Installation script for lldpd
- `show_heighbours.sh` - View LLDP neighbors information
- `neighors.txt` - Sample neighbor information

## Notes
- The script uses a 2-second timeout between polling attempts
- The service is stopped after capturing neighbor information
- All captured output is logged with timestamps for future reference
