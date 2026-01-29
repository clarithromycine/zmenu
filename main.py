"""
Example Console Application with Multi-Level Menus
Demonstrates the menu system with various options and submenus.
"""

from console_app import ConsoleApp

def main():

    try:
        # Setup and run the application
        app = ConsoleApp("ZMenu Demo App")
        app.run()
    except KeyboardInterrupt:
        # Handle Ctrl+C at the global level
        print("\n\n" + "=" * 60)
        print("  ⏹️  Application stopped by user")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
