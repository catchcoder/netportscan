#!/usr/bin/env python3
"""
Textual TUI for displaying output.txt on Raspberry Pi 3.5" screen
"""

import os
from pathlib import Path
from datetime import datetime
from textual.app import ComposeResult, RenderableType
from textual.containers import Container, Vertical
from textual.widgets import Static, Header, Footer, RichLog
from textual.binding import Binding
from textual.app import App
from textual.reactive import reactive
from rich.text import Text


class OutputDisplay(RichLog):
    """Widget to display file contents with scrolling"""
    
    file_path = reactive(Path(os.path.expanduser("output.txt")))
    last_modified = reactive(0.0)
    
    def __init__(self, file_path: str = "output.txt", **kwargs):
        super().__init__(**kwargs)
        self.file_path = Path(os.path.expanduser(file_path))
        self.last_content = ""
        self.load_file()
    
    def load_file(self) -> None:
        """Load content from file"""
        try:
            if self.file_path.exists():
                current_modified = self.file_path.stat().st_mtime
                
                # Only update if file has changed
                if current_modified != self.last_modified:
                    with open(self.file_path, 'r') as f:
                        content = f.read()
                    
                    # Only update if content actually changed
                    if content != self.last_content:
                        self.clear()
                        self.write(content)
                        self.last_content = content
                    
                    self.last_modified = current_modified
            else:
                self.write(Text(f"Waiting for {self.file_path}...", style="yellow"))
        except Exception as e:
            self.write(Text(f"Error reading file: {e}", style="red"))
    
    def set_file(self, file_path: str) -> None:
        """Switch to a different file"""
        self.file_path = Path(os.path.expanduser(file_path))
        self.last_modified = 0.0
        self.last_content = ""
        self.load_file()
    
    def on_mount(self) -> None:
        """Start auto-refresh when widget mounts"""
        self.set_interval(2, self.load_file)  # Refresh every 2 seconds


class OutputTUI(App):
    """Main TUI application for Raspberry Pi 3.5" screen"""
    
    CSS = """
    Screen {
        background: $surface;
        color: $text;
    }
    
    #output-container {
        width: 100%;
        height: 100%;
        border: solid $primary;
        padding: 0 1;
    }
    
    OutputDisplay {
        width: 100%;
        height: 100%;
        background: $background;
        color: $text;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("r", "refresh", "Refresh", show=True),
        Binding("o", "load_output", "Output", show=True),
        Binding("l", "load_log", "Log", show=True),
    ]
    
    TITLE = "Network Port Scan"
    
    def __init__(self, output_file: str = "output.txt"):
        super().__init__()
        self.output_file = output_file
        self.output_display = None
        self.current_file = output_file
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header(show_clock=True)
        
        with Container(id="output-container"):
            self.output_display = OutputDisplay(file_path=self.output_file)
            yield self.output_display
        
        yield Footer()
    
    def watch_title(self) -> None:
        """Update subtitle when current file changes"""
        file_name = Path(self.current_file).name
        self.sub_title = f"Viewing: {file_name}"
    
    def action_refresh(self) -> None:
        """Manual refresh action"""
        if self.output_display:
            self.output_display.load_file()
            self.notify("Refreshed", timeout=1.5)
    
    def action_load_output(self) -> None:
        """Load output.txt"""
        if self.output_display:
            self.current_file = "output.txt"
            self.output_display.set_file("~/output.txt")
            self.watch_title()
            self.notify("Switched to output.txt", timeout=1.5)
    
    def action_load_log(self) -> None:
        """Load lldp_log.txt"""
        if self.output_display:
            self.current_file = "lldp_log.txt"
            self.output_display.set_file("~/lldp_log.txt")
            self.watch_title()
            self.notify("Switched to lldp_log.txt", timeout=1.5)
    
    def on_mount(self) -> None:
        """Setup on app mount"""
        # Set theme for better small screen visibility
        self.theme = "nord"  # Or try "dracula", "gruvbox-dark", "solarized-dark"
        self.watch_title()


def main():
    """Run the TUI application"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Display output.txt or lldp_log.txt in Textual TUI")
    parser.add_argument("-f", "--file", default="output.txt", help="Path to output file (default: output.txt)")
    parser.add_argument("-l", "--log", action="store_true", help="Start with lldp_log.txt instead of output.txt")
    args = parser.parse_args()
    
    output_file = "~/lldp_log.txt" if args.log else f"~/{args.file}"
    app = OutputTUI(output_file=output_file)
    app.run()


if __name__ == "__main__":
    main()
