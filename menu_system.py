"""
Multi-level Menu System for Console Applications
A flexible and reusable menu framework supporting nested menus.
"""

from typing import Callable, Dict, List, Optional, Tuple
import os
import sys

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
    
    def __init__(self, cmd: str, desc: str, order: int = 0, label: Optional[str] = None, group: Optional[str] = None, icon: Optional[str] = None):

        self.cmd = cmd      #指令
        self.label = label or desc #界面显示的指令
        self.desc = desc    #描述
        self.order = order  #显示顺序        
        self.group = group  #分组
        self.icon = icon    #图标
    
    def __call__(self, fn: Callable) -> Callable:

        fn.cmd = self.cmd
        fn.label = self.label
        fn.desc = self.desc
        fn.order = self.order        
        fn.group = self.group
        fn.icon = self.icon
        return fn

class MenuItem:
    """Represents a single menu item."""    
    def __init__(self, label: str, action: Optional[Callable] = None):
        self.label = label
        self.action = action
    
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
    
    def add_item(self, key: str, label: str, action: Callable, icon: Optional[str] = None) -> None:
        """
        Add a menu item with an associated action.
        
        Args:
            key: Unique identifier for the item
            label: Display text
            action: Callable function to execute
        """
        if icon:
            label = icon + " " + label
        self.items[key] = MenuItem(label, action)        
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
                items_to_register.append((fn.order, fn.cmd, fn.label, fn, group, icon))
                        
        # Sort by order
        items_to_register.sort(key=lambda x: x[0])

        # Track created submenus
        submenus = {}
        
        # Register items, handling group parameter for nested menus
        for order, cmd, label, fn, group, icon in items_to_register:
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
                current_menu.add_item(cmd, label, fn, icon)
            else:
                # Add item to root menu                
                self.add_item(cmd, label, fn, icon)
    
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
        print("[Use Arrow Keys ↑↓ to navigate, Enter to select, type number, or ESC to go back]")
    
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
            # Highlight selected item
            if idx - 1 == selected_idx:
                print(f"  ➤ {idx}. {label} ◄")
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
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        if ch == '\x03':  # Ctrl+C
            raise KeyboardInterrupt()
        if ch == '\x1b':  # Escape sequence
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                next1 = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            
            if next1 == '[':
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    next2 = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                
                if next2 == 'A':
                    return ('NAV', 'UP')
                if next2 == 'B':
                    return ('NAV', 'DOWN')
                if next2 == 'C':
                    return ('NAV', 'RIGHT')
                if next2 == 'D':
                    return ('NAV', 'LEFT')

            return ('ESC', None)
        if ch in ('\r', '\n'):
            return ('ENTER', None)
        if ch.isdigit():
            return ('DIGIT', ch)
        return ('CHAR', ch)
    
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
        if clear_initial:
            os.system('cls' if os.name == 'nt' else 'clear')
        self._display_header(clear=False)
        self._display_items(selected_idx=selected_idx)
        print("[Use Arrow Keys ↑↓ to navigate, Enter to select, type number, or ESC to go back]")
        
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
                            selected_idx = (selected_idx - 1) % (max_idx + 1)
                            # Redraw menu in place
                            self._redraw_menu_in_place(selected_idx)
                            continue
                        elif ch2 == b'P':  # Down arrow
                            selected_idx = (selected_idx + 1) % (max_idx + 1)
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
                            selected_idx = (selected_idx - 1) % (max_idx + 1)
                        elif value == 'DOWN':
                            selected_idx = (selected_idx + 1) % (max_idx + 1)
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


class ConsoleApp:
    """Main console application with menu system."""
    
    def __init__(self, name: str = "Console App"):
        """
        Initialize the console application.
        
        Args:
            name: Application name
        """
        self.name = name
        self.main_menu = Menu(title=name)
    
    def get_menu(self) -> Menu:
        """Get the main menu for configuration."""
        return self.main_menu
    
    def run(self) -> None:
        """Run the console application."""
        self.main_menu.display()
        print("\n" + "=" * 60)
        print("  Thank you for using the application!")
        print("=" * 60 + "\n")


# Example actions for demonstration
def hello_world():
    """Simple hello world action."""
    print("\n👋 Hello from the console app!")
    return True


def user_greeting():
    """Get user input and display greeting."""
    name = input("\nEnter your name: ").strip()
    if name:
        print(f"\n👋 Hello, {name}! Nice to meet you.")
    return True


def show_calculator():
    """Simple calculator demonstration."""
    try:
        num1 = float(input("\nEnter first number: "))
        num2 = float(input("Enter second number: "))
        
        print(f"\n  {num1} + {num2} = {num1 + num2}")
        print(f"  {num1} - {num2} = {num1 - num2}")
        print(f"  {num1} × {num2} = {num1 * num2}")
        if num2 != 0:
            print(f"  {num1} ÷ {num2} = {num1 / num2}")
        else:
            print(f"  Division by zero not allowed")
    except ValueError:
        print("\n❌ Invalid number input")
    
    return True


def show_system_info():
    """Display system information."""
    print(f"\nOperating System: {sys.platform}")
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"Current Directory: {os.getcwd()}")
    return True


def show_about():
    """Show about information."""
    print("\n" + "=" * 60)
    print("  Multi-Level Menu Console Application")
    print("=" * 60)
    print("\nThis application demonstrates a flexible menu system")
    print("that supports multiple levels of nested menus.")
    print("\nFeatures:")
    print("  • Nested menu support")
    print("  • Easy to extend with new options")
    print("  • Clean, user-friendly interface")
    print("  • Error handling and input validation")
    print("=" * 60)
    return True
