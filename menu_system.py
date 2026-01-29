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
    
    def __init__(self, cmd: str, desc: str, order: int = 0, label: Optional[str] = None):
        """
        Initialize a menu item decorator.
        
        Args:
            cmd: Command identifier (unique key for the menu item)
            desc: Description/display label for the menu item
            order: Display order in menu (lower numbers appear first)
            label: Custom display label (if different from desc)
        """
        self.cmd = cmd
        self.desc = desc
        self.order = order
        self.label = label or desc
    
    def __call__(self, fn: Callable) -> Callable:
        """
        Attach metadata to the function and return it.
        
        Args:
            fn: Function to decorate
        
        Returns:
            The decorated function with attached metadata
        """
        fn.cmd = self.cmd
        fn.desc = self.desc
        fn.order = self.order
        fn.label = self.label
        return fn


class MenuItem:
    """Represents a single menu item."""
    
    def __init__(self, label: str, action: Optional[Callable] = None):
        """
        Initialize a menu item.
        
        Args:
            label: Display text for the menu item
            action: Callable function to execute, or None for submenu marker
        """
        self.label = label
        self.action = action
    
    def execute(self) -> bool:
        """
        Execute the menu item's action.
        
        Returns:
            True if should continue menu, False if should exit
        """
        if self.action is None:
            return True
        return self.action()


class Menu:
    """Represents a menu with multiple items and support for submenus."""
    
    def __init__(self, title: str = "Menu", parent: Optional['Menu'] = None):
        """
        Initialize a menu.
        
        Args:
            title: Display title for the menu
            parent: Parent menu (for navigation back)
        """
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
    
    def add_item(self, key: str, label: str, action: Callable) -> None:
        """
        Add a menu item with an associated action.
        
        Args:
            key: Unique identifier for the item
            label: Display text
            action: Callable function to execute
        """
        self.items[key] = MenuItem(label, action)
        self._item_order.append(key)
    
    def add_submenu(self, key: str, label: str, auto_icon = True) -> 'Menu':
        """
        Add a submenu and return it for further configuration.
        
        Automatically adds a folder icon (📁) to the label if auto_icon=True,
        or a custom icon if auto_icon is a string.
        
        Args:
            key: Unique identifier for the submenu
            label: Display text
            auto_icon: 
                - True: Use default folder icon (📁)
                - False: No icon
                - str: Use custom icon (e.g., "🛠️")
        
        Returns:
            The newly created submenu
        """
        # Add icon based on auto_icon parameter
        if auto_icon is True:
            # Use default folder icon
            folder_icon = "📁 "
            if not label.startswith(folder_icon):
                label = folder_icon + label
        elif isinstance(auto_icon, str):
            # Use custom icon (string) - first remove default folder icon if present
            folder_icon = "📁 "
            if label.startswith(folder_icon):
                label = label[len(folder_icon):]  # Remove folder icon
            
            custom_icon = auto_icon + " "
            if not label.startswith(custom_icon):
                label = custom_icon + label
        # If auto_icon is False, no icon is added
        
        submenu = Menu(title=label, parent=self)
        self.submenus[key] = submenu
        self.items[key] = MenuItem(label, None)
        self._item_order.append(key)
        return submenu
    
    def register(self, *functions: Callable) -> None:
        """
        Register decorated menu item functions.
        
        Registers functions decorated with @MenuItemCmd.
        Functions are sorted by order and added to the menu.
        Supports group parameter for nested menu organization with custom icons.
        
        Args:
            *functions: Functions decorated with @MenuItemCmd
        
        Example:
            @MenuItemCmd("greet", "👋 Say Hello", group="General", group_icon="📋")
            def hello():
                print("Hello!")
                return True
            
            menu.register(hello)
        """
        # Collect functions with cmd attribute and build group_icon mapping
        items_to_register = []
        group_icons = {}  # Track group_icon for each group path
        
        for fn in functions:
            if hasattr(fn, 'cmd'):
                group = getattr(fn, 'group', None)
                group_icon = getattr(fn, 'group_icon', None)
                items_to_register.append((fn.order, fn.cmd, fn.label, fn, group, group_icon))
                
                # Store the first group_icon found for each group (to avoid duplicates)
                if group and group_icon and group not in group_icons:
                    group_icons[group] = group_icon
        
        # Sort by order
        items_to_register.sort(key=lambda x: x[0])
        
        # Track created submenus
        submenus = {}
        
        # Register items, handling group parameter for nested menus
        for order, cmd, label, fn, group, group_icon in items_to_register:
            if group:
                # Split group path (e.g., "Tools.Advanced" -> ["Tools", "Advanced"])
                group_path = group.split('.')
                
                # Navigate/create nested menus
                current_menu = self
                for i, group_name in enumerate(group_path):
                    submenu_key = '.'.join(group_path[:i+1])
                    
                    if submenu_key not in submenus:
                        # Create submenu if it doesn't exist
                        # Use custom group_icon if provided for the final group level
                        # Otherwise use default folder icon (auto_icon=True)
                        if i == len(group_path) - 1 and submenu_key in group_icons:
                            # Use the mapped group_icon for this group
                            custom_icon = group_icons[submenu_key]
                            submenu = current_menu.add_submenu(submenu_key, group_name, auto_icon=custom_icon)
                        else:
                            # Use default folder icon
                            submenu = current_menu.add_submenu(submenu_key, group_name, auto_icon=True)
                        submenus[submenu_key] = submenu
                    else:
                        submenu = submenus[submenu_key]
                    
                    current_menu = submenu
                
                # Add item to the final submenu
                current_menu.add_item(cmd, label, fn)
            else:
                # Add item to root menu
                self.add_item(cmd, label, fn)
    
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
        print("[Use Arrow Keys ↑↓ to navigate, Enter to select, or type number]")
    
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
        
        # Check if we have a buffered character from previous ESC sequence
        if self._key_buffer is not None:
            ch = self._key_buffer
            self._key_buffer = None
        else:
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
                # Buffer the extra character for next read
                self._key_buffer = next2
            else:
                # Buffer the character that followed ESC
                self._key_buffer = next1
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
        print("[Use Arrow Keys ↑↓ to navigate, Enter to select, or type number]")
        
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
        elif idx == num_items + (1 if self.parent else 0):
            return '0'
        
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
