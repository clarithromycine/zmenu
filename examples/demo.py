"""
Demonstration script showing zmenu framework capabilities.
This script creates a menu and shows its output.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zmenu import Menu, MenuItem


def main():
    """Create and display menu structure."""
    
    # Create a nested menu structure to demonstrate unlimited depth
    
    # Level 3 - Deepest menu
    deep_menu = Menu("Deep Menu (Level 3)")
    deep_menu.add_action("Deep Action 1", lambda: print("Action executed!"))
    deep_menu.add_action("Deep Action 2", lambda: print("Another action!"))
    
    # Level 2 - Middle menu
    middle_menu = Menu("Middle Menu (Level 2)")
    middle_menu.add_action("Middle Action", lambda: print("Middle action!"))
    middle_menu.add_submenu("Go Deeper", deep_menu, "Navigate to level 3")
    
    # Level 1 - First submenu
    submenu = Menu("Settings (Level 1)")
    submenu.add_action("View Settings", lambda: print("Settings displayed"))
    submenu.add_submenu("Advanced Settings", middle_menu, "Access advanced options")
    
    # Level 0 - Main menu
    main_menu = Menu("Main Application Menu")
    main_menu.add_action("Quick Action", lambda: print("Quick action executed"))
    main_menu.add_submenu("Settings", submenu, "Configure application settings")
    main_menu.add_action("About", lambda: print("zmenu v0.1.0 - A flexible menu framework"))
    
    # Display the main menu once
    main_menu.display()
    print("\n" + "=" * 60)
    print("Framework Features Demonstrated:")
    print("=" * 60)
    print("✓ Clean, professional menu display")
    print("✓ Support for both actions and submenus")
    print("✓ Nested menus at unlimited depth (4 levels shown)")
    print("✓ Automatic back/exit navigation")
    print("✓ Method chaining for easy menu construction")
    print("✓ Optional descriptions for menu items")
    print("=" * 60)


if __name__ == "__main__":
    main()
