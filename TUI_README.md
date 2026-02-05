# Textual TUI - Output File Viewer

A lightweight Terminal User Interface (TUI) for displaying `output.txt` on a Raspberry Pi 3.5" screen using the Textual library.

## Features

- Reads and displays `output.txt` in real-time
- Auto-refreshes every 2 seconds when file is updated
- Optimized for small screens (3.5" displays)
- Keyboard shortcuts for quick actions
- Shows file update status
- Responsive and smooth scrolling

## Installation

Install required dependencies:

```bash
pip install textual
```

## Usage

### Basic Usage

Run the TUI viewer:

```bash
python3 tui.py
```

### With Custom Output File

Specify a different file to monitor:

```bash
python3 tui.py -f /path/to/your/output.txt
```

or

```bash
python3 tui.py --file /path/to/your/output.txt
```

## Keyboard Controls

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `r` | Manually refresh the output |
| `↑`/`↓` | Scroll up/down |
| `Page Up`/`Page Down` | Scroll faster |
| `Home`/`End` | Jump to start/end |

## How It Works

1. The script starts and reads `output.txt` (or specified file)
2. Content is displayed in a scrollable text area
3. Every 2 seconds, the script checks if the file has been modified
4. If modified (by your bash script), the content is automatically refreshed
5. The display updates with the new content

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

### File Not Found
Ensure `output.txt` is in the same directory as `tui.py`, or specify the full path:
```bash
python3 tui.py -f ~/output.txt
```

### Content Not Updating
- Check that your bash script is actually writing to the file
- Verify file permissions: `ls -la output.txt`
- Increase refresh interval in the code if needed

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
