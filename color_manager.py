"""
Color Scheme Manager for Console Applications
Centralized color and formatting control.
"""
import json
import os
from typing import Dict, Optional


class ColorScheme:
    """Manages console colors and ANSI escape codes."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize ColorScheme with configuration.
        
        Args:
            config_file: Path to color_scheme.json. If None, searches in standard locations.
        """
        self.config = {}
        self._load_config(config_file)
    
    def _load_config(self, config_file: Optional[str] = None) -> None:
        """Load color scheme configuration from JSON file.
        
        Args:
            config_file: Path to configuration file
        """
        if config_file is None:
            # Try to find color_scheme.json in common locations
            possible_paths = [
                os.path.join(os.path.dirname(__file__), 'color_scheme.json'),
                'color_scheme.json',
                os.path.expanduser('~/.zmenu/color_scheme.json'),
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    config_file = path
                    break
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load color scheme from {config_file}: {e}")
                self._set_defaults()
        else:
            self._set_defaults()
    
    def _set_defaults(self) -> None:
        """Set default color configuration."""
        self.config = {
            "colors": {
                "primary": {"code": "\033[38;5;208m", "name": "orange"},
                "secondary": {"code": "\033[90m", "name": "gray"},
                "reset": {"code": "\033[0m", "name": "reset"}
            },
            "cursor": {
                "hide": "\033[?25l",
                "show": "\033[?25h"
            },
            "cursor_movement": {
                "up": "\033[A",
                "down": "\033[B",
                "right": "\033[C",
                "left": "\033[D"
            },
            "screen": {
                "clear_line": "\033[2K",
                "clear_to_end": "\033[0J"
            }
        }
    
    def get_color(self, color_name: str) -> str:
        """Get ANSI code for a color.
        
        Args:
            color_name: Name of the color (e.g., 'primary', 'secondary', 'reset')
        
        Returns:
            ANSI escape code
        """
        if color_name in self.config.get('colors', {}):
            return self.config['colors'][color_name]['code']
        return ""
    
    def get_cursor(self, action: str) -> str:
        """Get ANSI code for cursor operation.
        
        Args:
            action: Action ('hide', 'show')
        
        Returns:
            ANSI escape code
        """
        if action in self.config.get('cursor', {}):
            return self.config['cursor'][action]
        return ""
    
    def get_cursor_move(self, direction: str, lines: int = 1) -> str:
        """Get ANSI code for cursor movement.
        
        Args:
            direction: Direction ('up', 'down', 'left', 'right')
            lines: Number of lines to move
        
        Returns:
            ANSI escape code
        """
        base_code = self.config.get('cursor_movement', {}).get(direction, '\033[A')
        return f"\033[{lines}{base_code[-1]}"
    
    def get_screen(self, action: str) -> str:
        """Get ANSI code for screen operation.
        
        Args:
            action: Action ('clear_line', 'clear_to_end')
        
        Returns:
            ANSI escape code
        """
        if action in self.config.get('screen', {}):
            return self.config['screen'][action]
        return ""
    
    def colorize(self, text: str, color: str = 'primary') -> str:
        """Apply color to text.
        
        Args:
            text: Text to colorize
            color: Color to apply
        
        Returns:
            Colorized text with reset code
        """
        color_code = self.get_color(color)
        reset_code = self.get_color('reset')
        if color_code:
            return f"{color_code}{text}{reset_code}"
        return text
    
    def get_highlight_item(self, label: str, long_desc: Optional[str] = None) -> str:
        """Format a highlighted menu item.
        
        Args:
            label: Item label
            long_desc: Optional long description
        
        Returns:
            Formatted highlighted item string
        """
        desc_text = ""
        if long_desc:
            secondary_code = self.get_color('secondary')
            reset_code = self.get_color('reset')
            desc_text = f" {secondary_code}({long_desc}){reset_code}"
        
        primary_code = self.get_color('primary')
        reset_code = self.get_color('reset')
        return f"  {primary_code}➤ {label}{desc_text} {reset_code}"
    
    def get_checkbox_item(self, checked: bool, label: str, highlighted: bool = False) -> str:
        """Format a checkbox item.
        
        Args:
            checked: Whether checkbox is checked
            label: Item label
            highlighted: Whether item is highlighted
        
        Returns:
            Formatted checkbox item string
        """
        checkbox = "[•]" if checked else "[ ]"
        
        if highlighted:
            primary_code = self.get_color('primary')
            reset_code = self.get_color('reset')
            return f"{primary_code}  {checkbox} {label}{reset_code}"
        else:
            return f"  {checkbox} {label}"
    
    def get_yes_no_text(self, selected_index: int) -> str:
        """Format yes/no selection text.
        
        Args:
            selected_index: 0 for YES, 1 for NO
        
        Returns:
            Formatted yes/no text
        """
        primary_code = self.get_color('primary')
        reset_code = self.get_color('reset')
        
        yes_text = f"{primary_code}➤ YES{reset_code}" if selected_index == 0 else "  YES"
        no_text = f"{primary_code}➤ NO{reset_code}" if selected_index == 1 else "  NO"
        
        return f"  {yes_text} / {no_text}"


# Global color scheme instance
_color_scheme = None


def get_color_scheme() -> ColorScheme:
    """Get or create the global color scheme instance.
    
    Returns:
        ColorScheme instance
    """
    global _color_scheme
    if _color_scheme is None:
        _color_scheme = ColorScheme()
    return _color_scheme


def initialize_color_scheme(config_file: Optional[str] = None) -> ColorScheme:
    """Initialize the global color scheme with optional config file.
    
    Args:
        config_file: Path to color_scheme.json
    
    Returns:
        ColorScheme instance
    """
    global _color_scheme
    _color_scheme = ColorScheme(config_file)
    return _color_scheme
