"""
Console Application with Menu System
Main application class for managing menus and application flow.
"""
import sys, os, inspect, datetime
from menu_system import Menu, MenuItemCmd
    
class ConsoleApp:
    """Main console application with menu system."""
            
    def __init__(self, name: str = "Console App"):
        self.name = name
        self.main_menu = Menu(title=name)
        self.setup_menu()

    def setup_menu(self) -> None:
        """Setup and register all menu items."""
        main_menu = self.main_menu
        
        decorated_methods = []
        members = inspect.getmembers(self, predicate=inspect.ismethod)
        for name, method in members:
            if hasattr(method, 'cmd'):  
                decorated_methods.append(method)
        
        main_menu.register(*decorated_methods)
        
        for group_path, (icon, display_name) in self.MENU_GROUP_ICONS.items():
            
            path_parts = group_path.split('.')
            current_menu = main_menu
            
            for i in range(len(path_parts) - 1):
                submenu_key = '.'.join(path_parts[:i+1])
                if submenu_key in current_menu.submenus:
                    current_menu = current_menu.submenus[submenu_key]
            
            final_key = path_parts[-1] if len(path_parts) == 1 else '.'.join(path_parts)
            
            if final_key in current_menu.items:
                current_menu.items[final_key].label = f"{icon} {display_name} >"


    
    def run(self) -> None:
        self.main_menu.display()

    # Group icons configuration for visual customization
    # Maps group path to icon and display name
    MENU_GROUP_ICONS = {
        "Tools":            ("🛠️", "Tools"),
        "Settings":         ("⚙️", "Settings"),
        "Settings.Display": ("📺", "Display Options"),
        "Settings.Language":("🌐", "Language"),
        "Help":             ("📖", "Help")
    }

    # Menu item action methods
    @MenuItemCmd("greeting", "Say Hello", order=0, icon="👋", long_desc="Display a friendly greeting message")
    def hello_world(self):
        """Simple hello world action."""
        print("\n👋 Hello from the console app!")
        return True

    @MenuItemCmd("user", "Greet User", order=1, icon="👤", long_desc="Ask for user name and display personalized greeting")
    def user_greeting(self):
        """Get user input and display greeting."""
        name = input("\nEnter your name: ").strip()
        if name:
            print(f"\n👋 Hello, {name}! Nice to meet you.")
        return True

    @MenuItemCmd("calc", "Calculator", order=0, group="Tools", icon="🧮", long_desc="Perform basic arithmetic operations")
    def show_calculator(self):
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

    @MenuItemCmd("sysinfo", "System Information", order=1, group="Tools", icon="ℹ️", long_desc="Display system and environment details")
    def show_system_info(self):
        """Display system information."""
        print(f"\nOperating System: {sys.platform}")
        print(f"Python Version: {sys.version.split()[0]}")
        print(f"Current Directory: {os.getcwd()}")
        return True

    @MenuItemCmd("about", "About", order=0, group="Help", icon="📖", long_desc="Learn about this application")
    def show_about(self):
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

    @MenuItemCmd("theme", "Change Theme", group="Settings.Display", icon="🎨", long_desc="Customize the visual appearance")
    def show_theme_options(self):
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

    @MenuItemCmd("font", "Change Font Size", group="Settings.Display", icon="🔠", long_desc="Adjust text size for better readability")
    def show_font_options(self):
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

    @MenuItemCmd("en", "English", group="Settings.Language", long_desc="Set interface language to English")
    def set_language_en(self):
        """Set language to English."""
        print(f"\n✅ Language changed to: English")
        return True

    @MenuItemCmd("es", "Español", group="Settings.Language", long_desc="Cambiar idioma de interfaz al español")
    def set_language_es(self):
        """Set language to Español."""
        print(f"\n✅ Language changed to: Español")
        return True

    @MenuItemCmd("fr", "Français", group="Settings.Language", long_desc="Définir la langue de l'interface au français")
    def set_language_fr(self):
        """Set language to Français."""
        print(f"\n✅ Language changed to: Français")
        return True

    @MenuItemCmd("status", "System Status", order=1, icon="📊", long_desc="Check the current operational status of the application")
    def show_status(self):
        """Display application status."""
        print("\n" + "=" * 60)
        print("  SYSTEM STATUS")
        print("=" * 60)
        print("\n  ✓ Application running normally")
        print("  ✓ All systems operational")
        print("  ✓ Ready for commands")
        return True

    @MenuItemCmd("time", "Show Time", order=2, icon="🕐", long_desc="Display the current date and time")
    def show_time(self):
        """Display current time."""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n  Current time: {current_time}")
        return True

    @MenuItemCmd("usage", "How to Use", group="Help", icon="❓", long_desc="Learn how to navigate and use this application")
    def show_usage(self):
        """Show usage instructions."""
        print("\n" + "=" * 60)
        print("  HOW TO USE")
        print("=" * 60 + "\n")
        print("1. Navigate using menu numbers or arrow keys")
        print("2. Press ESC to exit the current menu or application")
        print("3. Follow on-screen prompts for actions")
        print("\nExample Navigation:")
        print("  Main Menu → Tools → Calculator")
        print("           → Settings → Display → Theme")
        print("           → Help → About")
        return True

    @MenuItemCmd("keyboard", "Keyboard Shortcuts", group="Help", icon="⌨️", long_desc="View available keyboard shortcuts and navigation keys")
    def show_shortcuts(self):
        """Show keyboard shortcuts."""
        print("\n" + "=" * 60)
        print("  KEYBOARD SHORTCUTS")
        print("=" * 60)
        print("\n  0 - Exit current menu or application")
        print("  1-9 - Navigate to menu option (depends on menu size)")
        print("  ESC - Go back to parent menu (or exit at root menu)")
        print("\n  Note: Shortcuts are number-based for menu navigation")
        return True
    @MenuItemCmd("confirm", "Confirm Demo", order=3, icon="✓", long_desc="Test the yes/no selection with arrow keys")
    def confirm_demo(self):
        """Demonstrate the yes/no prompt with left/right arrow keys."""
        result = self.main_menu.yes_no_prompt(
            question="Do you want to continue?",
            description="Use LEFT/RIGHT arrow keys to select, then press ENTER"
        )
        
        if result is True:
            print("\n✓ You selected: YES")
        elif result is False:
            print("\n✗ You selected: NO")
        else:
            print("\n⊘ You cancelled the operation")
        
        return True