"""
Console Application with Menu System
Main application class for managing menus and application flow.
"""

from typing import Callable, Optional
import sys
import os
from menu_system import Menu, MenuItemCmd
    
class ConsoleApp:
    """Main console application with menu system."""
    
    # Group icons configuration for visual customization
    # Maps group path to icon and display name
    MENU_GROUP_ICONS = {
        "Tools":            ("🛠️", "Tools"),
        "Settings":         ("⚙️", "Settings"),
        "Settings.Display": ("📺", "Display Options"),
        "Settings.Language":("🌐", "Language"),
        "Help":             ("📖", "Help")
    }
        
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



# Example actions for demonstration
@MenuItemCmd("greeting", "Say Hello", order=0, icon="👋")
def hello_world():
    """Simple hello world action."""
    print("\n👋 Hello from the console app!")
    return True


@MenuItemCmd("user", "Greet User", order=1, icon="👤")
def user_greeting():
    """Get user input and display greeting."""
    name = input("\nEnter your name: ").strip()
    if name:
        print(f"\n👋 Hello, {name}! Nice to meet you.")
    return True


@MenuItemCmd("calc", "Calculator", order=0, group="Tools",icon="🧮")
def show_calculator():
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


@MenuItemCmd("sysinfo", "System Information", order=1, group="Tools",icon="ℹ️")
def show_system_info():
    """Display system information."""
    print(f"\nOperating System: {sys.platform}")
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"Current Directory: {os.getcwd()}")
    return True


@MenuItemCmd("about", "About", order=0, group="Help",icon="📖")
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


@MenuItemCmd("theme", "Change Theme", group="Settings.Display", icon="🎨")
def show_theme_options():
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


@MenuItemCmd("font", "Change Font Size", group="Settings.Display", icon="🔠")
def show_font_options():
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


@MenuItemCmd("en", "English", group="Settings.Language")
def set_language_en():
    """Set language to English."""
    print(f"\n✅ Language changed to: English")
    return True


@MenuItemCmd("es", "Español", group="Settings.Language")
def set_language_es():
    """Set language to Español."""
    print(f"\n✅ Language changed to: Español")
    return True


@MenuItemCmd("fr", "Français", group="Settings.Language")
def set_language_fr():
    """Set language to Français."""
    print(f"\n✅ Language changed to: Français")
    return True


@MenuItemCmd("status", "System Status", order=1, icon="📊")
def show_status():
    """Display application status."""
    print("\n" + "=" * 60)
    print("  SYSTEM STATUS")
    print("=" * 60)
    print("\n  ✓ Application running normally")
    print("  ✓ All systems operational")
    print("  ✓ Ready for commands")
    return True


@MenuItemCmd("time", "Show Time", order=2, icon="🕐")
def show_time():
    """Display current time."""
    import datetime
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n  Current time: {current_time}")
    return True


@MenuItemCmd("usage", "How to Use", group="Help", icon="❓")
def show_usage():
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


@MenuItemCmd("keyboard", "Keyboard Shortcuts", group="Help", icon="⌨️")
def show_shortcuts():
    """Show keyboard shortcuts."""
    print("\n" + "=" * 60)
    print("  KEYBOARD SHORTCUTS")
    print("=" * 60)
    print("\n  0 - Exit current menu or application")
    print("  1-9 - Navigate to menu option (depends on menu size)")
    print("  ESC - Go back to parent menu (or exit at root menu)")
    print("\n  Note: Shortcuts are number-based for menu navigation")
    return True
