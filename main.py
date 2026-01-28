"""
Example Console Application with Multi-Level Menus
Demonstrates the menu system with various options and submenus.
"""

from menu_system import ConsoleApp, hello_world, user_greeting, show_calculator
from menu_system import show_system_info, show_about


def setup_application() -> ConsoleApp:
    """
    Configure the console application with menus and actions.
    
    Returns:
        Configured ConsoleApp instance
    """
    app = ConsoleApp("My Console Application")
    main_menu = app.get_menu()
    
    # Add main menu items
    main_menu.add_item("greeting", "👋 Say Hello", hello_world)
    main_menu.add_item("user", "👤 Greet User", user_greeting)
    
    # Add Tools submenu
    # Use clear_screen_after_action=False to keep output visible after actions
    tools_menu = main_menu.add_submenu("tools", "🛠️  Tools", clear_screen_after_action=True)
    tools_menu.add_item("calc", "Calculator", show_calculator)
    tools_menu.add_item("sysinfo", "System Information", show_system_info)
    
    # Add Settings submenu
    settings_menu = main_menu.add_submenu("settings", "⚙️  Settings")
    
    # Add nested submenus under Settings
    display_menu = settings_menu.add_submenu("display", "Display Options")
    display_menu.add_item("theme", "Change Theme", lambda: _show_theme_options())
    display_menu.add_item("font", "Change Font Size", lambda: _show_font_options())
    
    language_menu = settings_menu.add_submenu("language", "Language")
    language_menu.add_item("en", "English", lambda: _set_language("English"))
    language_menu.add_item("es", "Español", lambda: _set_language("Español"))
    language_menu.add_item("fr", "Français", lambda: _set_language("Français"))
    
    # Add Help submenu
    help_menu = main_menu.add_submenu("help", "❓ Help")
    help_menu.add_item("about", "About", show_about)
    help_menu.add_item("usage", "How to Use", _show_usage)
    help_menu.add_item("keyboard", "Keyboard Shortcuts", _show_shortcuts)
    
    return app


def _show_theme_options():
    """Display theme options."""
    print("\n" + "=" * 60)
    print("  THEME OPTIONS")
    print("=" * 60)
    print("\n  Available themes:")
    print("    • Light")
    print("    • Dark")
    print("    • High Contrast")
    print("\n  [This is a demonstration - feature not fully implemented]")
    return True


def _show_font_options():
    """Display font size options."""
    print("\n" + "=" * 60)
    print("  FONT SIZE OPTIONS")
    print("=" * 60)
    print("\n  Available sizes:")
    print("    • Small (8pt)")
    print("    • Medium (12pt)")
    print("    • Large (16pt)")
    print("\n  [This is a demonstration - feature not fully implemented]")
    return True


def _set_language(language: str):
    """Set the application language."""
    print(f"\n✅ Language changed to: {language}")
    return True


def _show_usage():
    """Show usage instructions."""
    print("\n" + "=" * 60)
    print("  HOW TO USE")
    print("=" * 60)
    print("\n1. Navigate using menu numbers")
    print("2. Press 0 to exit the current menu or application")
    print("3. Use 'Back' option to return to previous menu")
    print("4. Follow on-screen prompts for actions")
    print("\nExample Navigation:")
    print("  Main Menu → Tools → Calculator")
    print("           → Settings → Display → Theme")
    print("           → Help → About")
    return True


def _show_shortcuts():
    """Show keyboard shortcuts."""
    print("\n" + "=" * 60)
    print("  KEYBOARD SHORTCUTS")
    print("=" * 60)
    print("\n  0 - Exit current menu or application")
    print("  1-9 - Navigate to menu option (depends on menu size)")
    print("\n  Note: Shortcuts are number-based for menu navigation")
    return True


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
        print("  ⏹️  Application interrupted by user (Ctrl+C)")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
