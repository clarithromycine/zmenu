"""
Console Application with Menu System
Main application class for managing menus and application flow.
"""

from menu_system import Menu


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
