"""
Simple example demonstrating basic menu usage.
"""

from zmenu import Menu, MenuItem


def hello_world():
    """Simple hello world action."""
    print("\nHello, World!")
    print("This is a simple action example.")


def greet_user():
    """Interactive greeting action."""
    name = input("\nWhat's your name? ")
    print(f"\nHello, {name}! Nice to meet you!")


def show_info():
    """Display information action."""
    print("\n" + "=" * 50)
    print("zmenu - Interactive Console Menu Framework")
    print("=" * 50)
    print("\nFeatures:")
    print("- Unlimited nested menu depth")
    print("- Simple and intuitive API")
    print("- Easy to extend and customize")
    print("- Clean console interface")


def main():
    """Create and run a simple menu."""
    # Create the main menu
    menu = Menu("Simple Menu Example")
    
    # Add menu items
    menu.add_action("Say Hello", hello_world)
    menu.add_action("Greet User", greet_user)
    menu.add_action("Show Information", show_info)
    
    # Run the menu
    menu.run()


if __name__ == "__main__":
    main()
