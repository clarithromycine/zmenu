"""
Multi-level Menu System for Console Applications
A flexible and reusable menu framework supporting nested menus.
"""

from typing import Callable, Dict, List, Optional, Tuple
import os
import sys

try:    
    import fcntl
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False

try:
    import msvcrt
    import sys as sys_module
    HAS_MSVCRT = True
except ImportError:
    HAS_MSVCRT = False

try:
    import curses
    HAS_CURSES = True
except ImportError:
    HAS_CURSES = False

try:
    import termios
    import tty
    HAS_TERMIOS = True
except ImportError:
    HAS_TERMIOS = False



class MenuItemCmd:
    """Decorator for defining menu items with metadata."""
    
    def __init__(self, cmd: str, desc: str, order: int = 0, label: Optional[str] = None, group: Optional[str] = None, icon: Optional[str] = None, long_desc: Optional[str] = None):

        self.cmd = cmd      #指令
        self.label = label or desc #界面显示的指令
        self.desc = desc    #描述
        self.long_desc = long_desc  #长描述
        self.order = order  #显示顺序        
        self.group = group  #分组
        self.icon = icon    #图标
    
    def __call__(self, fn: Callable) -> Callable:

        fn.cmd   = self.cmd
        fn.label = self.label
        fn.desc  = self.desc
        fn.long_desc = self.long_desc
        fn.order = self.order        
        fn.group = self.group
        fn.icon  = self.icon
        return fn

class MenuItem:
    """Represents a single menu item."""    
    def __init__(self, label: str, action: Optional[Callable] = None, long_desc: Optional[str] = None):
        self.label = label
        self.action = action
        self.long_desc = long_desc
    
    def execute(self) -> bool:
        if self.action is None:
            return True
        return self.action()


class Menu:
    """Represents a menu with multiple items and support for submenus."""    
    def __init__(self, title: str = "Menu", parent: Optional['Menu'] = None):

        self.title = title
        self.parent = parent
        self.items: Dict[str, MenuItem] = {}
        self.submenus: Dict[str, 'Menu'] = {}
        self._item_order: List[str] = []
    
    def _hide_cursor(self) -> None:
        """Hide the cursor using ANSI escape codes."""
        sys.stdout.write('\033[?25l')
        sys.stdout.flush()
    
    def _show_cursor(self) -> None:
        """Show the cursor using ANSI escape codes."""
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()
    
    def _clear_screen(self) -> None:
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def add_item(self, key: str, label: str, action: Callable, icon: Optional[str] = None, long_desc: Optional[str] = None) -> None:
        """
        Add a menu item with an associated action.
        
        Args:
            key: Unique identifier for the item
            label: Display text
            action: Callable function to execute
            icon: Optional icon character
            long_desc: Optional long description text
        """
        if icon:
            label = icon + " " + label
        self.items[key] = MenuItem(label, action, long_desc)        
        self._item_order.append(key)
    
    def add_submenu(self, key: str, label: str, icon: Optional[str] = None) -> 'Menu':
        
        if icon:
            label = icon + " " + label
            
        submenu = Menu(title=label, parent=self)
        self.submenus[key] = submenu
        self.items[key] = MenuItem(label, None)
        self._item_order.append(key)
        return submenu
    
    def register(self, *functions: Callable) -> None:

        # Collect functions with cmd attribute and build group_icon mapping
        items_to_register = []        
        
        for fn in functions:
            if hasattr(fn, 'cmd'):
                group = getattr(fn, 'group', None)                
                icon  = getattr(fn, 'icon', None)
                long_desc = getattr(fn, 'long_desc', None)
                items_to_register.append((fn.order, fn.cmd, fn.label, fn, group, icon, long_desc))
                        
        # Sort by order
        items_to_register.sort(key=lambda x: x[0])

        # Track created submenus
        submenus = {}
        
        # Register items, handling group parameter for nested menus
        for order, cmd, label, fn, group, icon, long_desc in items_to_register:
            if group:
                # Split group path (e.g., "Tools.Advanced" -> ["Tools", "Advanced"])
                group_path = group.split('.')
                
                # Navigate/create nested menus
                current_menu = self
                for i, group_name in enumerate(group_path):
                    submenu_key = '.'.join(group_path[:i+1])
                    
                    if submenu_key not in submenus:
                        submenu = current_menu.add_submenu(submenu_key, group_name+" >")
                        submenus[submenu_key] = submenu
                    else:
                        submenu = submenus[submenu_key]
                    
                    current_menu = submenu
                
                # Add item to the final submenu
                current_menu.add_item(cmd, label, fn, icon, long_desc)
            else:
                # Add item to root menu                
                self.add_item(cmd, label, fn, icon, long_desc)
    
    def _redraw_menu_in_place(self, selected_idx: int = 0) -> None:
        """Redraw only the menu items in place.
        
        Args:
            selected_idx: Index of the currently selected item
        """
        num_items = len(self._item_order)
        # Count lines: items + back option (if parent) + instruction line
        total_menu_lines = num_items + (1 if self.parent else 0) + 1
        
        # Move cursor up to the start of menu items (skip header)
        sys.stdout.write(f'\033[{total_menu_lines}A')  # Move up N lines
        sys.stdout.flush()
        
        # Clear from cursor to end of screen
        sys.stdout.write('\033[0J')
        sys.stdout.flush()
        
        # Redraw menu items
        self._display_items(selected_idx=selected_idx)
        print("[Use Arrow Keys ↑↓ to navigate, Enter to select]")
    
    def _display_header(self, clear: bool = True) -> None:
        """Display the menu header.
        
        Args:
            clear: Whether to clear the screen before displaying
        """
        if clear:
            self._clear_screen()
        print("\n" + "=" * 60)
        print(f"  {self.title.upper()}")
        print("=" * 60 + "\n")
    
    def _display_items(self, selected_idx: int = 0) -> None:
        """Display all menu items with optional highlighting.
        
        Args:
            selected_idx: Index of the currently selected item (0-based)
        """
        num_items = len(self._item_order)
        back_idx = num_items
        
        for idx, key in enumerate(self._item_order, 1):
            label = self.items[key].label
            long_desc = self.items[key].long_desc
            
            # Highlight selected item with description
            if idx - 1 == selected_idx:
                desc_text = f" \033[90m({long_desc})\033[0m" if long_desc else ""
                print(f"  \033[38;5;208m➤ {idx}. {label}{desc_text} \033[0m")
            else:
                print(f"    {idx}. {label}")
        
        # Show back option if there's a parent menu
        if self.parent:
            if back_idx == selected_idx:
                print(f"  ➤ {num_items + 1}. Back to {self.parent.title} ◄")
            else:
                print(f"    {num_items + 1}. Back to {self.parent.title}")

    def _read_key_posix(self) -> Optional[Tuple[str, Optional[str]]]:
        """Read a single keypress on POSIX systems using raw terminal input."""
        if not HAS_TERMIOS:
            return None
        
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
                    return ('ESC', None)
                
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
                        return ('NAV', 'UP')
                    if next2 == 'B':
                        return ('NAV', 'DOWN')
                    if next2 == 'C':
                        return ('NAV', 'RIGHT')
                    if next2 == 'D':
                        return ('NAV', 'LEFT')
                
                # Not an arrow key, just ESC
                return ('ESC', None)
            
            if ch in ('\r', '\n'):
                return ('ENTER', None)
            if ch.isdigit():
                return ('DIGIT', ch)
            return ('CHAR', ch)
        finally:
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)  # Restore original flags
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def _redraw_multi_select_in_place(self, items: List[dict], selected_idx: int) -> None:
        """Redraw the multi-select list in place.
        
        Args:
            items: List of {label, description, selected} dicts
            selected_idx: Current selected index
        """
        # Move cursor up to start of list (items + instruction + blank = num_items + 2)
        num_items = len(items)
        sys.stdout.write(f'\033[{num_items + 2}A')  # Move up all items + blank + instruction
        
        # Redraw all items
        for idx, item in enumerate(items):
            checkbox = "[•]" if item['selected'] else "[ ]"
            highlight = "\033[38;5;208m" if idx == selected_idx else ""
            reset = "\033[0m" if idx == selected_idx else ""
            label = item['label']
            
            sys.stdout.write('\033[2K')  # Clear entire line
            sys.stdout.write(f"\r{highlight}  {checkbox} {label}{reset}\n")
        
        # Move down to instruction line
        sys.stdout.write(f'\033[{num_items}B')
        sys.stdout.flush()
    
    def multi_select_prompt(self, title: str, items: List[dict], allow_empty: bool = False) -> List[dict]:
        """Display a multi-select prompt with checkboxes.
        
        Args:
            title: Title to display
            items: List of {label, description, selected} dicts
            allow_empty: Whether to allow all items to be deselected
        
        Returns:
            List of selected items
        """
        self._hide_cursor()
        try:
            selected_idx = 0
            
            # Display header
            print("\n  " + title)
            
            # Display items
            for idx, item in enumerate(items):
                checkbox = "[•]" if item['selected'] else "[ ]"
                highlight = "\033[38;5;208m" if idx == selected_idx else ""
                reset = "\033[0m" if idx == selected_idx else ""
                label = item['label']
                
                print(f"{highlight}  {checkbox} {label}{reset}")
            
            print("\n[Use Arrow Keys ↑↓ to navigate, SPACE to toggle, Enter to confirm]")
            
            while True:
                try:
                    if HAS_MSVCRT and os.name == 'nt':
                        ch = msvcrt.getch()
                        
                        if ch == b'\x03':  # Ctrl+C
                            raise KeyboardInterrupt()
                        
                        if ch == b'\xe0':  # Extended key
                            ch2 = msvcrt.getch()
                            if ch2 == b'H':  # Up arrow
                                selected_idx = (selected_idx - 1) % len(items)
                                self._redraw_multi_select_in_place(items, selected_idx)
                                continue
                            elif ch2 == b'P':  # Down arrow
                                selected_idx = (selected_idx + 1) % len(items)
                                self._redraw_multi_select_in_place(items, selected_idx)
                                continue
                        elif ch == b' ':  # Space to toggle
                            items[selected_idx]['selected'] = not items[selected_idx]['selected']
                            self._redraw_multi_select_in_place(items, selected_idx)
                            continue
                        elif ch == b'\r':  # Enter to confirm
                            return [item for item in items if item['selected']]
                        elif ch == b'\x1b':  # Escape
                            return None
                    
                    elif HAS_TERMIOS and sys.stdin.isatty():
                        key_info = self._read_key_posix()
                        if not key_info:
                            continue
                        kind, value = key_info
                        
                        if kind == 'NAV':
                            if value == 'UP':
                                selected_idx = (selected_idx - 1) % len(items)
                                self._redraw_multi_select_in_place(items, selected_idx)
                            elif value == 'DOWN':
                                selected_idx = (selected_idx + 1) % len(items)
                                self._redraw_multi_select_in_place(items, selected_idx)
                            continue
                        if kind == 'CHAR' and value == ' ':  # Space to toggle
                            items[selected_idx]['selected'] = not items[selected_idx]['selected']
                            self._redraw_multi_select_in_place(items, selected_idx)
                            continue
                        if kind == 'ENTER':
                            return [item for item in items if item['selected']]
                        if kind == 'ESC':
                            return None
                    else:
                        choice = input("\nPress SPACE to toggle, Enter to confirm: ").strip()
                        if choice == '':
                            return [item for item in items if item['selected']]
                        
                except KeyboardInterrupt:
                    raise
        finally:
            self._show_cursor()
    
    def _redraw_yes_no_in_place(self, selected: int) -> None:
        """Redraw only the yes/no selection line in place.
        
        Args:
            selected: 0 for YES, 1 for NO
        """
        yes_text = f"\033[38;5;208m➤ YES\033[0m" if selected == 0 else "  YES"
        no_text = f"\033[38;5;208m➤ NO\033[0m" if selected == 1 else "  NO"
        # Move cursor up 3 lines to YES/NO line, clear it, and reprint
        sys.stdout.write('\033[3A')  # Move up 3 lines
        sys.stdout.write('\033[2K')  # Clear the line
        sys.stdout.write('\r')       # Return to start of line
        sys.stdout.write(f"  {yes_text} / {no_text}\n")
        sys.stdout.write('\033[3B')  # Move down 3 lines back to input position
        sys.stdout.flush()
    
    def yes_no_prompt(self, question: str = "Do you want to continue?", description: str = "") -> bool:
        """Display a yes/no prompt with left/right arrow key selection.
        
        Args:
            question: The question to display
            description: Optional description to display
        
        Returns:
            True if user selects "Yes", False if "No"
        """
        self._hide_cursor()
        try:
            selected = 0  # 0 = Yes, 1 = No
            
            # Display header once
            print("\n" + "=" * 60)
            print(f"  {question}")
            print("=" * 60)
            if description:
                print(f"\n{description}")
            print()
            
            first_time = True
            
            while True:
                # Display yes/no (first time normally, then update in place)
                if first_time:
                    yes_text = f"\033[38;5;208m➤ YES\033[0m" if selected == 0 else "  YES"
                    no_text = f"\033[38;5;208m➤ NO\033[0m" if selected == 1 else "  NO"
                    print(f"  {yes_text} / {no_text}")
                    print("\n[Use Arrow Keys ← → to select, Enter to confirm]")
                    first_time = False
                
                # Get input
                try:
                    if HAS_MSVCRT and os.name == 'nt':
                        ch = msvcrt.getch()
                        
                        if ch == b'\x03':  # Ctrl+C
                            raise KeyboardInterrupt()
                        
                        if ch == b'\xe0':  # Extended key
                            ch2 = msvcrt.getch()
                            if ch2 == b'K':  # Left arrow
                                if selected != 0:
                                    selected = 0
                                    self._redraw_yes_no_in_place(selected)
                                continue
                            elif ch2 == b'M':  # Right arrow
                                if selected != 1:
                                    selected = 1
                                    self._redraw_yes_no_in_place(selected)
                                continue
                        elif ch == b'\r':  # Enter
                            return selected == 0
                        elif ch == b'\x1b':  # Escape
                            return None
                    
                    elif HAS_TERMIOS and sys.stdin.isatty():
                        key_info = self._read_key_posix()
                        if not key_info:
                            continue
                        kind, value = key_info
                        
                        if kind == 'NAV':
                            if value == 'LEFT':
                                if selected != 0:
                                    selected = 0
                                    self._redraw_yes_no_in_place(selected)
                            elif value == 'RIGHT':
                                if selected != 1:
                                    selected = 1
                                    self._redraw_yes_no_in_place(selected)
                            continue
                        if kind == 'ENTER':
                            return selected == 0
                        if kind == 'ESC':
                            return None
                    else:
                        choice = input("\nEnter Y/N: ").strip().upper()
                        if choice == 'Y':
                            return True
                        elif choice == 'N':
                            return False
                        
                except KeyboardInterrupt:
                    raise
        finally:
            self._show_cursor()
    
    def _get_user_choice(self, clear_initial: bool = True) -> Optional[str]:
        """
        Get user's menu choice with keyboard navigation support.
        
        Args:
            clear_initial: Whether to clear screen on initial display
        
        Returns:
            The key of selected item or None if invalid
        """
        num_items = len(self._item_order)
        max_idx = num_items + (1 if self.parent else 0)
        selected_idx = 0
        
        # Initial display
        #if clear_initial:
        #    os.system('cls' if os.name == 'nt' else 'clear')
        self._display_header(clear=False)
        self._display_items(selected_idx=selected_idx)
        print("[Use Arrow Keys ↑↓ to navigate, Enter to select]")
        
        while True:
            # Get input
            try:
                # Windows arrow-key handling via msvcrt
                if HAS_MSVCRT and os.name == 'nt':
                    ch = msvcrt.getch()
                    
                    # Check for Ctrl+C
                    if ch == b'\x03':
                        raise KeyboardInterrupt()
                    
                    if ch == b'\xe0':  # Extended key
                        ch2 = msvcrt.getch()
                        if ch2 == b'H':  # Up arrow
                            selected_idx = (selected_idx - 1) % max_idx
                            # Redraw menu in place
                            self._redraw_menu_in_place(selected_idx)
                            continue
                        elif ch2 == b'P':  # Down arrow
                            selected_idx = (selected_idx + 1) % max_idx
                            # Redraw menu in place
                            self._redraw_menu_in_place(selected_idx)
                            continue
                    elif ch == b'\x1b':  # Escape key
                        if self.parent:
                            return 'back'
                        else:
                            raise KeyboardInterrupt()
                    elif ch == b'\r':  # Enter - return without clearing
                        return self._index_to_key(selected_idx)
                    elif ch.isdigit():
                        choice = ch.decode().strip()
                        try:
                            choice_num = int(choice)
                            if 1 <= choice_num <= num_items:
                                return self._item_order[choice_num - 1]
                            elif self.parent and choice_num == num_items + 1:
                                return 'back'
                        except ValueError:
                            pass
                # POSIX raw terminal handling
                elif HAS_TERMIOS and sys.stdin.isatty():
                    key_info = self._read_key_posix()
                    if not key_info:
                        continue
                    kind, value = key_info
                    if kind == 'NAV':
                        if value == 'UP':
                            selected_idx = (selected_idx - 1) % max_idx
                        elif value == 'DOWN':
                            selected_idx = (selected_idx + 1) % max_idx
                        self._redraw_menu_in_place(selected_idx)
                        continue
                    if kind == 'ESC':
                        if self.parent:
                            return 'back'
                        else:
                            raise KeyboardInterrupt()
                    if kind == 'ENTER':
                        return self._index_to_key(selected_idx)
                    if kind == 'DIGIT':
                        try:
                            choice_num = int(value)
                            if 1 <= choice_num <= num_items:
                                return self._item_order[choice_num - 1]
                            elif self.parent and choice_num == num_items + 1:
                                return 'back'
                        except ValueError:
                            continue
                else:
                    # Generic fallback when raw key handling is unavailable
                    choice = input("\nEnter your choice: ").strip()
                    return self._process_choice(choice)
                    
            except KeyboardInterrupt:
                # Re-raise to allow Ctrl+C to work
                raise
            except (ValueError, IndexError):
                pass
    
    def _index_to_key(self, idx: int) -> Optional[str]:
        """Convert selected index to menu key.
        
        Args:
            idx: Selected index
        
        Returns:
            Menu item key or None
        """
        num_items = len(self._item_order)
        
        if 0 <= idx < num_items:
            return self._item_order[idx]
        elif self.parent and idx == num_items:
            return 'back'
        
        return None
    
    def _process_choice(self, choice: str) -> Optional[str]:
        """Process numeric choice input.
        
        Args:
            choice: User's numeric input
        
        Returns:
            Menu item key or None if invalid
        """
        if self.parent and choice == str(len(self._item_order) + 1):
            return 'back'
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(self._item_order):
                return self._item_order[choice_num - 1]
            
            max_choice = len(self._item_order) + (1 if self.parent else 0)
            print(f"\n⚠️  Invalid choice. Please enter a number between 1 and {max_choice}")
            input("Press Enter to continue...")
            return None
            
        except (ValueError, IndexError):
            print("\n⚠️  Invalid input. Please enter a valid number.")
            input("Press Enter to continue...")
            return None
    
    def _execute_choice(self, key: str) -> bool:
        """
        Execute the selected menu item or submenu.
        
        Args:
            key: The key of the selected item
        
        Returns:
            True to continue showing this menu, False to exit
        """
        if key == 'back':
            return False
        
        # Check if it's a submenu
        if key in self.submenus:
            self.submenus[key].display(clear_first=False)
            return True
        
        # Execute regular menu item
        if key in self.items:
            try:
                result = self.items[key].execute()
                if result is False:
                    return False
            except Exception as e:
                print(f"\n❌ Error executing action: {e}")
            
            input("\nPress Enter to continue...")
            return True
        
        return True
    
    def display(self, clear_first: bool = True) -> None:
        """Display the menu and handle user interaction.
        
        Args:
            clear_first: Whether to clear screen on first display
        """
        try:
            while True:
                self._hide_cursor()  # Hide cursor during menu navigation
                choice = self._get_user_choice(clear_initial=clear_first)
                self._show_cursor()  # Show cursor before executing choice
                
                if choice is None:
                    continue
                
                if not self._execute_choice(choice):
                    break
                
                # After first interaction, don't clear on next menu display
                clear_first = False
        finally:
            self._show_cursor()  # Ensure cursor is shown when exiting menu










