"""
Multi-level Menu System for Console Applications
A flexible and reusable menu framework supporting nested menus.
"""

from typing import Callable, Dict, List, Optional, Tuple
import os
import sys
import json
from ansi_manager import get_ansi_scheme
from input_handler import read_key_as_tuple



class MenuItemCmd:
    """Decorator for defining menu items with metadata.
    
    Menu configuration is loaded from menu_config.json.
    Only cmd parameter is needed here.
    """
    
    def __init__(self, cmd: str):
        self.cmd = cmd
    
    def __call__(self, fn: Callable) -> Callable:
        fn.cmd = self.cmd
        # Other attributes will be loaded from menu_config.json in Menu.register()
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
        ansi = get_ansi_scheme()
        sys.stdout.write(ansi.get_cursor('hide'))
        sys.stdout.flush()
    
    def _show_cursor(self) -> None:
        """Show the cursor using ANSI escape codes."""
        ansi = get_ansi_scheme()
        sys.stdout.write(ansi.get_cursor('show'))
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
    
    def add_submenu(self, key: str, label: str, icon: Optional[str] = None, long_desc: Optional[str] = None) -> 'Menu':
        
        if icon:
            label = icon + " " + label
            
        submenu = Menu(title=label, parent=self)
        self.submenus[key] = submenu
        self.items[key] = MenuItem(label, None, long_desc)
        self._item_order.append(key)
        return submenu
    
    @staticmethod
    def load_menu_config(config_path: Optional[str] = None) -> Dict:
        """Load menu configuration from JSON file.
        
        Args:
            config_path: Path to menu_config.json. If None, searches in current directory.
        
        Returns:
            Dictionary with 'menu' key containing hierarchical menu structure
        """
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'menu_config.json')
        
        if not os.path.exists(config_path):
            return {'menu': []}
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except Exception as e:
            print(f"Warning: Failed to load menu config from {config_path}: {e}")
            return {'menu': []}
    
    def register(self, *functions: Callable, allowed_groups: Dict = None, config_path: Optional[str] = None) -> None:
        """Register menu items from decorated functions with hierarchical JSON configuration.
        
        Menu structure is defined in JSON following the display order.
        Items can be either:
        - Items with 'cmd': action items with decorated functions
        - Items with 'name': submenu groups containing 'items'
        
        Args:
            functions: Functions decorated with @MenuItemCmd
            allowed_groups: (Deprecated) kept for backward compatibility
            config_path: Path to menu_config.json
        """
        # Load menu configuration from JSON
        menu_config = self.load_menu_config(config_path)
        menu_items = menu_config.get('menu', [])
        
        # Build a map of cmd -> function for quick lookup
        cmd_to_fn = {}
        for fn in functions:
            if hasattr(fn, 'cmd'):
                cmd_to_fn[fn.cmd] = fn
        
        # Recursively register menu items following JSON hierarchy
        def register_menu_items(menu_list: List, current_menu: 'Menu') -> None:
            """Recursively register items from menu list into the specified menu.
            
            Args:
                menu_list: List of menu items from JSON
                current_menu: The Menu object to register items into
            """
            for item_config in menu_list:
                cmd = item_config.get('cmd')
                name = item_config.get('name')
                icon = item_config.get('icon', '')
                label = item_config.get('label', '')
                desc = item_config.get('desc', '')
                subitems = item_config.get('items', [])
                
                if cmd:  # This is an action item
                    fn = cmd_to_fn.get(cmd)
                    if fn:
                        item_label = label or cmd
                        current_menu.add_item(cmd, item_label, fn, icon, desc)
                
                elif name and subitems:  # This is a submenu
                    # Create submenu - pass icon in icon param, not in label
                    # add_submenu will handle adding icon to label
                    submenu = current_menu.add_submenu(name, name + " >", icon, desc)
                    # Recursively register subitems
                    register_menu_items(subitems, submenu)
        
        # Start registering from the top level
        register_menu_items(menu_items, self)
    
    def _redraw_menu_in_place(self, selected_idx: int = 0) -> None:
        """Redraw only the menu items in place.
        
        Args:
            selected_idx: Index of the currently selected item
        """
        ansi = get_ansi_scheme()
        num_items = len(self._item_order)
        # Count lines: items + back option (if parent) + instruction line
        total_menu_lines = num_items + (1 if self.parent else 0) + 1
        
        # Move cursor up to the start of menu items (skip header)
        sys.stdout.write(ansi.get_cursor_move('up', total_menu_lines))
        sys.stdout.flush()
        
        # Clear from cursor to end of screen
        sys.stdout.write(ansi.get_screen('clear_to_end'))
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
        ansi = get_ansi_scheme()
        num_items = len(self._item_order)
        back_idx = num_items
        primary_code = ansi.get_theme_color('primary')
        secondary_code = ansi.get_theme_color('secondary')
        reset_code = ansi.get_reset()
                
        for idx, key in enumerate(self._item_order, 1):
            label = self.items[key].label
            long_desc = self.items[key].long_desc
            
            # Highlight selected item with description
            if idx - 1 == selected_idx:
                desc_text = ""
                if long_desc:                                        
                    desc_text = f" {secondary_code}({long_desc}){reset_code}"                                
                print(f"  {primary_code}➤ {idx}. {label}{desc_text} {reset_code}")
            else:
                print(f"    {idx}. {label}")
        
        # Show back option if there's a parent menu
        if self.parent:
            if back_idx == selected_idx:                
                print(f"  {primary_code}➤ {num_items + 1}. Back to {self.parent.title} {reset_code}")
            else:
                print(f"    {num_items + 1}. Back to {self.parent.title}")

    def _redraw_multi_select_in_place(self, items: List[dict], selected_idx: int) -> None:
        """Redraw the multi-select list in place.
        
        Args:
            items: List of {label, description, selected} dicts
            selected_idx: Current selected index
        """
        ansi = get_ansi_scheme()
        # Move cursor up to start of list (items + instruction + blank = num_items + 2)
        num_items = len(items)
        sys.stdout.write(ansi.get_cursor_move('up', num_items + 2))
        
        # Redraw all items
        for idx, item in enumerate(items):
            checkbox = "[•]" if item['selected'] else "[ ]"
            highlight = ansi.get_theme_color('primary')            
            reset = ansi.get_reset()

            label = item['label']
            
            sys.stdout.write(ansi.get_screen('clear_line'))  # Clear entire line

            if idx == selected_idx:
                print(f"{highlight}  {checkbox} {label}{reset}")
            else:
                print(f"  {checkbox} {label}")
                    
        # Move down to instruction line
        sys.stdout.write(ansi.get_cursor_move('down', num_items))
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
        ansi = get_ansi_scheme()
        self._hide_cursor()
        try:
            selected_idx = 0
            
            # Display header
            print("\n  " + title)
            
            # Display items
            for idx, item in enumerate(items):
                checkbox = "[•]" if item['selected'] else "[ ]"
                highlight = ansi.get_theme_color('primary') if idx == selected_idx else ""
                reset = ansi.get_reset() if idx == selected_idx else ""
                label = item['label']
                
                print(f"{highlight}  {checkbox} {label}{reset}")
            
            print("\n[Use Arrow Keys ↑↓ to navigate, SPACE to toggle, Enter to confirm]")
            
            while True:
                try:
                    key_info = read_key_as_tuple()
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
                    if kind == 'SPACE':  # Space to toggle
                        items[selected_idx]['selected'] = not items[selected_idx]['selected']
                        self._redraw_multi_select_in_place(items, selected_idx)
                        continue
                    if kind == 'ENTER':
                        return [item for item in items if item['selected']]
                    if kind == 'ESC':
                        return None
                        
                except KeyboardInterrupt:
                    raise
        finally:
            self._show_cursor()
    
    def _redraw_yes_no_in_place(self, selected: int) -> None:
        """Redraw only the yes/no selection line in place.
        
        Args:
            selected: 0 for YES, 1 for NO
        """
        ansi = get_ansi_scheme()
        yes_text = f"{ansi.get_theme_color('primary')}➤ YES{ansi.get_reset()}" if selected == 0 else "  YES"
        no_text = f"{ansi.get_theme_color('primary')}➤ NO{ansi.get_reset()}" if selected == 1 else "  NO"
        # Move cursor up 3 lines to YES/NO line, clear it, and reprint
        sys.stdout.write(ansi.get_cursor_move('up', 3))  # Move up 3 lines
        sys.stdout.write(ansi.get_screen('clear_line'))  # Clear the line
        sys.stdout.write('\r')       # Return to start of line
        sys.stdout.write(f"  {yes_text} / {no_text}\n")
        sys.stdout.write(ansi.get_cursor_move('down', 3))  # Move down 3 lines back to input position
        sys.stdout.flush()
    
    def yes_no_prompt(self, question: str = "Do you want to continue?", description: str = "") -> bool:
        """Display a yes/no prompt with left/right arrow key selection.
        
        Args:
            question: The question to display
            description: Optional description to display
        
        Returns:
            True if user selects "Yes", False if "No"
        """
        ansi = get_ansi_scheme()
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
                    yes_text = f"{ansi.get_theme_color('primary')}➤ YES{ansi.get_reset()}" if selected == 0 else "  YES"
                    no_text = f"{ansi.get_theme_color('primary')}➤ NO{ansi.get_reset()}" if selected == 1 else "  NO"
                    print(f"  {yes_text} / {no_text}")
                    print("\n[Use Arrow Keys ← → to select, Enter to confirm]")
                    first_time = False
                
                # Get input
                try:
                    key_info = read_key_as_tuple()
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
                key_info = read_key_as_tuple()
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










