#!/usr/bin/env python3
"""
Textual TUI for displaying output.txt on Raspberry Pi 3.5" screen
"""

import os
from pathlib import Path
from datetime import datetime
from textual.app import ComposeResult, RenderableType
from textual.containers import Container, Vertical
from textual.widgets import Static, Header, Footer
from textual.binding import Binding
from textual.app import App
from textual.reactive import reactive


class OutputDisplay(Static):
    """Widget to display the contents of output.txt"""
    
    content = reactive("")
    file_path = reactive(Path(os.path.expanduser("output.txt")))
    last_modified = reactive(0.0)
    
    def __init__(self, file_path: str = "output.txt", **kwargs):
        super().__init__(**kwargs)
        self.file_path = Path(os.path.expanduser(file_path))
        self.last_content = ""
        self.load_file()
    
    def load_file(self) -> None:
        """Load content from output.txt"""
        try:
            if self.file_path.exists():
                current_modified = self.file_path.stat().st_mtime
                
                # Only update if file has changed
                if current_modified != self.last_modified:
                    with open(self.file_path, 'r') as f:
                        self.content = f.read()
                    self.last_modified = current_modified
            else:
                self.content = f"[yellow]Waiting for {self.file_path}...[/yellow]"
        except Exception as e:
            self.content = f"[red]Error reading file: {e}[/red]"
    
    def render(self) -> RenderableType:
        """Render the output.txt content"""
        return self.content
    
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
        overflow: auto;
        background: $background;
        color: $text;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("r", "refresh", "Refresh", show=True),
    ]
    
    TITLE = "Network Port Scan"
    SUB_TITLE = "Output Viewer"
    
    def __init__(self, output_file: str = "output.txt"):
        super().__init__()
        self.output_file = output_file
        self.output_display = None
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header(show_clock=True)
        
        with Container(id="output-container"):
            self.output_display = OutputDisplay(file_path=self.output_file)
            yield self.output_display
        
        yield Footer()
    
    def action_refresh(self) -> None:
        """Manual refresh action"""
        if self.output_display:
            self.output_display.load_file()
            self.notify("Refreshed output.txt", timeout=2)
    
    def on_mount(self) -> None:
        """Setup on app mount"""
        # Set theme for better small screen visibility
        self.theme = "nord"  # Or try "dracula", "gruvbox-dark", "solarized-dark"


def main():
    """Run the TUI application"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Display output.txt in Textual TUI")
    parser.add_argument("-f", "--file", default="output.txt", help="Path to output file (default: output.txt)")
    args = parser.parse_args()
    
    app = OutputTUI(output_file=args.file)
    app.run()


if __name__ == "__main__":
    main()
