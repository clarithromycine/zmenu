"""
Core menu classes for zmenu framework.
"""

import os
import sys
from typing import Callable, List, Optional, Any


class MenuItem:
    """Represents a single menu item with an action or submenu."""
    
    def __init__(
        self,
        title: str,
        action: Optional[Callable] = None,
        submenu: Optional['Menu'] = None,
        description: str = ""
    ):
        """
        Initialize a MenuItem.
        
        Args:
            title: The display text for this menu item
            action: A callable to execute when this item is selected
            submenu: A submenu to navigate to when this item is selected
            description: Optional description text
        """
        self.title = title
        self.action = action
        self.submenu = submenu
        self.description = description
        
        if action and submenu:
            raise ValueError("MenuItem cannot have both an action and a submenu")
    
    def execute(self) -> Optional['Menu']:
        """
        Execute this menu item's action or return its submenu.
        
        Returns:
            The submenu if this item has one, None otherwise
        """
        if self.submenu:
            return self.submenu
        elif self.action:
            self.action()
        return None


class Menu:
    """Represents a menu with items and navigation support."""
    
    def __init__(
        self,
        title: str,
        items: Optional[List[MenuItem]] = None,
        parent: Optional['Menu'] = None
    ):
        """
        Initialize a Menu.
        
        Args:
            title: The title displayed at the top of the menu
            items: List of MenuItem objects
            parent: The parent menu (for navigation back)
        """
        self.title = title
        self.items = items or []
        self.parent = parent
        self._exit_requested = False
    
    def add_item(self, item: MenuItem) -> 'Menu':
        """
        Add a menu item to this menu.
        
        Args:
            item: The MenuItem to add
            
        Returns:
            Self for method chaining
        """
        self.items.append(item)
        return self
    
    def add_submenu(self, title: str, submenu: 'Menu', description: str = "") -> 'Menu':
        """
        Add a submenu to this menu.
        
        Args:
            title: The title for the submenu item
            submenu: The submenu to navigate to
            description: Optional description text
            
        Returns:
            Self for method chaining
        """
        submenu.parent = self
        item = MenuItem(title=title, submenu=submenu, description=description)
        self.items.append(item)
        return self
    
    def add_action(
        self,
        title: str,
        action: Callable,
        description: str = ""
    ) -> 'Menu':
        """
        Add an action item to this menu.
        
        Args:
            title: The title for the menu item
            action: The callable to execute when selected
            description: Optional description text
            
        Returns:
            Self for method chaining
        """
        item = MenuItem(title=title, action=action, description=description)
        self.items.append(item)
        return self
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display(self):
        """Display the menu to the console."""
        self.clear_screen()
        print(f"\n{'=' * 60}")
        print(f"{self.title:^60}")
        print(f"{'=' * 60}\n")
        
        for idx, item in enumerate(self.items, start=1):
            if item.description:
                print(f"{idx}. {item.title} - {item.description}")
            else:
                print(f"{idx}. {item.title}")
        
        if self.parent:
            print(f"\n0. Back to previous menu")
        else:
            print(f"\n0. Exit")
        
        print(f"\n{'=' * 60}")
    
    def get_choice(self) -> Optional[int]:
        """
        Get user's menu choice.
        
        Returns:
            The selected menu index or None if invalid
        """
        try:
            choice = input("\nEnter your choice: ").strip()
            return int(choice)
        except (ValueError, EOFError, KeyboardInterrupt):
            return None
    
    def run(self) -> Optional[Any]:
        """
        Run the menu loop.
        
        Returns:
            The result of the menu interaction
        """
        while not self._exit_requested:
            self.display()
            choice = self.get_choice()
            
            if choice is None:
                print("\nInvalid input. Please try again.")
                input("\nPress Enter to continue...")
                continue
            
            if choice == 0:
                if self.parent:
                    # Go back to parent menu
                    return None
                else:
                    # Exit application
                    self._exit_requested = True
                    print("\nGoodbye!")
                    return None
            
            if 1 <= choice <= len(self.items):
                item = self.items[choice - 1]
                result = item.execute()
                
                if result:  # If there's a submenu
                    result.run()  # Run the submenu
                else:
                    # Action was executed, pause before continuing
                    input("\nPress Enter to continue...")
            else:
                print(f"\nInvalid choice. Please select 1-{len(self.items)} or 0.")
                input("\nPress Enter to continue...")
        
        return None
    
    def exit(self):
        """Request exit from the menu loop."""
        self._exit_requested = True
        if self.parent:
            self.parent.exit()
