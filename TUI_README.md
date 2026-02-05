# Textual TUI - Output File Viewer

A lightweight Terminal User Interface (TUI) for displaying `output.txt` and `lldp_log.txt` on a Raspberry Pi 3.5" screen using the Textual library. Features automatic scrolling and real-time file monitoring.

## Features

- Reads and displays `output.txt` or `lldp_log.txt` in real-time
- Auto-refreshes every 2 seconds when files are updated
- Built-in vertical scrolling with RichLog widget
- Switch between multiple files with keyboard shortcuts
- Optimized for small screens (3.5" displays)
- Shows current file being viewed in subtitle
- Responsive interface with clean display
- Auto-clears old content and displays new updates

## Installation

Install required dependencies:

```bash
pip install textual
```

## Usage

### Basic Usage - Display output.txt

Run the TUI viewer (defaults to `output.txt`):

```bash
python3 tui.py
```

### Load lldp_log.txt Automatically

Start with the historical log file:

```bash
python3 tui.py -l
# or
python3 tui.py --log
```

### With Custom Output File

Specify a different file to monitor:

```bash
python3 tui.py -f /path/to/your/file.txt
# or
python3 tui.py --file /path/to/your/file.txt
```

### Switching Between Files in App

Once the app is running, use keyboard shortcuts to switch files:

- Press `o` to view `output.txt` (real-time updates)
- Press `l` to view `lldp_log.txt` (historical data)

## Keyboard Controls

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `r` | Manually refresh the current file |
| `o` | Switch to `output.txt` (real-time output) |
| `l` | Switch to `lldp_log.txt` (historical log) |
| `↑`/`↓` | Scroll up/down |
| `Page Up`/`Page Down` | Scroll faster |
| `Home`/`End` | Jump to start/end |

## How It Works

1. The script starts and reads `output.txt` (or specified file)
2. Content is displayed in a scrollable RichLog widget with automatic vertical scrolling
3. Every 2 seconds, the script checks if the file has been modified
4. If modified (by your bash script), the content is automatically refreshed
5. The display updates with new content and auto-scrolls to show updates
6. Press `o` or `l` to switch between `output.txt` and `lldp_log.txt`

### File Types

- **output.txt** - Real-time output from your bash script. Auto-refreshes on file changes.
- **lldp_log.txt** - Historical log of all LLDP discoveries with timestamps. Append-only file.

## Integration with Bash Scripts

Your bash script can write to `output.txt` like this:

```bash
#!/bin/bash

# Your command that produces output
lldpctl "$interface" > output.txt

# Or append to the file
echo "New data: $(date)" >> output.txt
```

The TUI will automatically detect the update and display the new content.

## Viewing the Log File

### Automatic Vertical Scrollbar

The TUI uses the RichLog widget which provides automatic scrolling capabilities:

- **Scroll with arrow keys** - Use `↑`/`↓` to scroll line by line
- **Page scrolling** - Use `Page Up`/`Page Down` for larger jumps
- **Jump to end** - Press `End` to skip to the end of the log
- **Jump to beginning** - Press `Home` to go to the start

### Viewing lldp_log.txt

The historical log file contains all LLDP discoveries with timestamps:

```bash
python3 tui.py --log
```

Or press `l` while the app is running to switch to the log file.

The log file shows a complete history of all LLDP neighbor discoveries, with entries like:
```
2026-02-05 14:23:45
SysName: switch-name
PortID: eth0
PortDescr: Uplink to Core
VLAN: 10,20,30
---
2026-02-05 14:28:30
SysName: switch-name-2
...
```

## Optimization for 3.5" Screen

### Screen Resolution
The 3.5" Raspberry Pi screen typically has resolutions like:
- 480x320 (common)
- 800x480 (some variants)

The TUI automatically adapts to your screen size.

### Tips for Better Readability

1. **Increase Font Size** - Adjust your terminal font in `/boot/config.txt`:
   ```
   framebuffer_height=480
   framebuffer_width=800
   ```

2. **Use Light Theme** - Edit `tui.py` and change the theme:
   ```python
   self.theme = "dracula"  # Try: nord, lightbulb, solarized-light
   ```

3. **Full Screen Mode** - The app runs full screen by default

4. **Reduce Content Size** - Limit output in your bash script:
   ```bash
   lldpctl "$interface" | head -30 > output.txt  # Only first 30 lines
   ```

## Configuration

Edit `tui.py` to customize:

### Change Refresh Interval

Find this line:
```python
self.set_interval(2, self.load_file)  # Refresh every 2 seconds
```

Change `2` to your desired refresh frequency in seconds.

### Change Theme

Modify the `on_mount` method:
```python
self.theme = "nord"  # Other options: dracula, gruvbox-dark, solarized-dark, lightbulb
```

## Troubleshooting

### File Not Found (output.txt)
Ensure `output.txt` is in the same directory as `tui.py`, or specify the full path:
```bash
python3 tui.py -f ~/output.txt
```

### Log File Not Available (lldp_log.txt)
The log file is created when `restart_lldpd.sh` runs for the first time:
- Run your LLDP script first: `sudo bash restart_lldpd.sh`
- Or use `tui.py` which will show "Waiting for ~/lldp_log.txt..." until it exists
- Once created, press `l` to view it in the app

### Content Not Updating
- Check that your bash script is actually writing to the file
- Verify file permissions: `ls -la output.txt`
- Increase refresh interval in the code if needed
- Manual refresh: Press `r` to force refresh the current file

### Scrolling Issues
- If text isn't scrolling, ensure the content is longer than the display height
- Press `End` to jump to the latest content
- Use `Page Down` for faster scrolling

### Performance Issues
- Reduce refresh frequency from 2 seconds to higher value
- Limit output file size in your bash script
- Use `head` or `tail` to show only relevant lines

### Terminal Issues
- Ensure terminal is at least 40x10 characters
- Use full-screen terminal for best experience
- Try different terminal emulator if issues persist

## Example: Complete Setup

1. Create bash script that generates output:
   ```bash
   #!/bin/bash
   while true; do
       echo "=== $(date) ===" > output.txt
       lldpctl enp0s13f0u2u2 >> output.txt
       sleep 5
   done
   ```

2. Run the TUI in another terminal:
   ```bash
   python3 tui.py
   ```

3. The TUI will display updates in real-time as your bash script writes to `output.txt`

4. Switch between files:
   - Press `o` to view current output
   - Press `l` to view the historical log

## Example: Dual Monitor Setup

Monitor both output and log simultaneously:

```bash
# Terminal 1: Run continuous LLDP discovery (outputs to both files)
sudo bash restart_lldpd.sh

# Terminal 2: View real-time output
python3 tui.py

# Terminal 3: View historical log with vertical scrolling
python3 tui.py --log
```

Or use `o`/`l` keys to switch between files in the same terminal.

## Advanced: Running Headlessly

To run the TUI on startup without a manual terminal:

1. Create systemd service in `/etc/systemd/system/tui.service`:
   ```ini
   [Unit]
   Description=Network Port Scan TUI
   After=network.target
   
   [Service]
   Type=simple
   User=pi
   WorkingDirectory=/home/pi/netportscan
   ExecStart=/usr/bin/python3 /home/pi/netportscan/tui.py
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

   Or to start with the log file:
   ```ini
   ExecStart=/usr/bin/python3 /home/pi/netportscan/tui.py --log
   ```

2. Enable and start:
   ```bash
   sudo systemctl enable tui.service
   sudo systemctl start tui.service
   ```

## References

- [Textual Documentation](https://textual.textualize.io/)
- [Textual Widgets](https://textual.textualize.io/guide/widgets/)
- [Textual Bindings](https://textual.textualize.io/guide/input/)

## Related Files

- [restart_lldpd.sh](restart_lldpd.sh) - Bash script that can generate output.txt
- [README.md](README.md) - Project overview
