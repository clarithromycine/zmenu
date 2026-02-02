"""
Unified Input/Key Handler for Console Applications
Provides consistent keyboard input handling across platforms and modules.
"""

import os
import sys
from typing import Optional, Tuple

try:    
    import fcntl
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False

try:
    import msvcrt
    HAS_MSVCRT = True
except ImportError:
    HAS_MSVCRT = False

try:
    import termios
    import tty
    HAS_TERMIOS = True
except ImportError:
    HAS_TERMIOS = False


def read_key() -> str:
    """
    Read a single keypress from user input (cross-platform).
    
    Returns standardized key strings:
    - Navigation: 'up', 'down', 'left', 'right'
    - Editing: 'enter', 'space', 'esc'
    - Character: 'char:{ch}'
    - Other: 'unknown'
    
    Raises:
        KeyboardInterrupt: When Ctrl+C is pressed
    """
    # Windows arrow-key handling via msvcrt
    if HAS_MSVCRT and os.name == 'nt':
        ch = msvcrt.getch()
        
        if ch == b'\x03':  # Ctrl+C
            raise KeyboardInterrupt()
        
        if ch == b'\xe0':  # Extended key (arrow keys, etc.)
            ch2 = msvcrt.getch()
            if ch2 == b'H':  # Up arrow
                return 'up'
            elif ch2 == b'P':  # Down arrow
                return 'down'
            elif ch2 == b'K':  # Left arrow
                return 'left'
            elif ch2 == b'M':  # Right arrow
                return 'right'
            return 'unknown'
        elif ch == b'\r':  # Enter
            return 'enter'
        elif ch == b' ':  # Space
            return 'space'
        elif ch == b'\x1b':  # Escape
            return 'esc'
        else:
            return f'char:{ch.decode(errors="ignore")}'
    
    # POSIX raw terminal handling
    elif HAS_TERMIOS and sys.stdin.isatty():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        try:
            tty.setraw(fd)
            # First character - read immediately
            ch = sys.stdin.read(1)
            
            if ch == '\x03':  # Ctrl+C
                raise KeyboardInterrupt()
            
            if ch == '\x1b':  # Escape sequence - try to read more without blocking
                # Temporarily set non-blocking mode
                fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)
                try:
                    next1 = sys.stdin.read(1)
                except BlockingIOError:
                    next1 = ''
                finally:
                    fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)  # Restore blocking mode
                
                if not next1:
                    # No follow-up char = bare ESC press
                    return 'esc'
                
                if next1 == '[':
                    # Try to read arrow key indicator
                    fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)
                    try:
                        next2 = sys.stdin.read(1)
                    except BlockingIOError:
                        next2 = ''
                    finally:
                        fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)
                    
                    if next2 == 'A':
                        return 'up'
                    if next2 == 'B':
                        return 'down'
                    if next2 == 'C':
                        return 'right'
                    if next2 == 'D':
                        return 'left'
                
                # Not an arrow key, just ESC
                return 'esc'
            
            if ch in ('\r', '\n'):
                return 'enter'
            if ch == ' ':
                return 'space'
            return f'char:{ch}'
        finally:
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)  # Restore original flags
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    else:
        # Fallback: use input() for generic systems
        inp = input().strip()
        if inp == '':
            return 'unknown'
        return f'char:{inp[0]}'


def read_key_as_tuple() -> Optional[Tuple[str, Optional[str]]]:
    """
    Read a single keypress and return as (kind, value) tuple.
    
    This format is compatible with menu_system's _read_key_posix() output.
    
    Returns:
        Tuple[kind, value]:
        - ('NAV', 'UP'|'DOWN'|'LEFT'|'RIGHT')
        - ('ENTER', None)
        - ('SPACE', None)
        - ('ESC', None)
        - ('DIGIT', '0'-'9')
        - ('CHAR', character)
        - None if no input
    
    Raises:
        KeyboardInterrupt: When Ctrl+C is pressed
    """
    key = read_key()
    
    if key.startswith('char:'):
        ch = key[5:]
        if ch.isdigit():
            return ('DIGIT', ch)
        return ('CHAR', ch)
    elif key == 'up':
        return ('NAV', 'UP')
    elif key == 'down':
        return ('NAV', 'DOWN')
    elif key == 'left':
        return ('NAV', 'LEFT')
    elif key == 'right':
        return ('NAV', 'RIGHT')
    elif key == 'enter':
        return ('ENTER', None)
    elif key == 'space':
        return ('SPACE', None)
    elif key == 'esc':
        return ('ESC', None)
    else:
        return None
