"""
Example Console Application with Multi-Level Menus
Demonstrates the menu system with various options and submenus.
"""

import inspect
import console_app
from console_app import ConsoleApp


def setup_application() -> ConsoleApp:

    app = ConsoleApp("ZMenu Demo App")
    main_menu = app.get_menu()
    
    # Auto-scan console_app module for @MenuItemCmd decorated functions
    decorated_functions = []
    members = inspect.getmembers(console_app, predicate=inspect.isfunction)
    for name, fn in members:
        if hasattr(fn, 'cmd'):  # Check if function has MenuItemCmd decorator
            decorated_functions.append(fn)
    
    # Register all discovered menu items
    # The group parameter automatically creates nested menu structure
    main_menu.register(*decorated_functions)
    
    # Apply group icons from app's GROUP_ICONS configuration if it exists
    if hasattr(app, 'MENU_GROUP_ICONS'):
        for group_path, (icon, display_name) in app.MENU_GROUP_ICONS.items():
            # Navigate to the correct menu level
            path_parts = group_path.split('.')
            current_menu = main_menu
            
            # Navigate to parent menu if nested
            for i in range(len(path_parts) - 1):
                submenu_key = '.'.join(path_parts[:i+1])
                if submenu_key in current_menu.submenus:
                    current_menu = current_menu.submenus[submenu_key]
            
            # Get the final key
            final_key = path_parts[-1] if len(path_parts) == 1 else '.'.join(path_parts)
            

                
            if final_key in current_menu.items:
                current_menu.items[final_key].label = f"{icon} {display_name} >"
    
    return app


def main():
    """Main entry point of the application."""
    print("\n" + "=" * 60)
    print("  INITIALIZING APPLICATION...")
    print("=" * 60)
    
    try:
        # Setup and run the application
        app = setup_application()
        app.run()
    except KeyboardInterrupt:
        # Handle Ctrl+C at the global level
        print("\n\n" + "=" * 60)
        print("  ⏹️  Application stopped by user")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
