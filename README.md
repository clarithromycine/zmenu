# zmenu

A flexible and reusable Python framework for building interactive console applications with nested menu support at unlimited depth levels.

## Features

- **Unlimited Nested Depth**: Create menu hierarchies as deep as you need
- **Simple and Intuitive API**: Easy to learn and use
- **Method Chaining**: Build menus fluently with chainable methods
- **Clean Console Interface**: Professional-looking menu displays
- **Flexible Actions**: Support for both callable actions and submenus
- **Built-in Navigation**: Automatic back/exit navigation handling

## Installation

Clone the repository and install the package:

```bash
git clone https://github.com/clarithromycine/zmenu.git
cd zmenu
pip install -e .
```

## Quick Start

Here's a simple example to get you started:

```python
from zmenu import Menu

def hello_world():
    print("\nHello, World!")

# Create a menu
menu = Menu("My Application")
menu.add_action("Say Hello", hello_world)
menu.run()
```

## Usage

### Creating a Simple Menu

```python
from zmenu import Menu

def greet():
    name = input("What's your name? ")
    print(f"Hello, {name}!")

def show_info():
    print("This is zmenu - an interactive menu framework")

# Create menu
menu = Menu("Main Menu")
menu.add_action("Greet User", greet)
menu.add_action("Show Info", show_info)

# Run the menu
menu.run()
```

### Creating Nested Menus

```python
from zmenu import Menu

# Create submenus
settings_menu = Menu("Settings")
settings_menu.add_action("Change Theme", lambda: print("Theme changed"))
settings_menu.add_action("Update Profile", lambda: print("Profile updated"))

# Create main menu with submenu
main_menu = Menu("Application")
main_menu.add_submenu("Settings", settings_menu, "Configure application")
main_menu.add_action("Exit", lambda: None)

main_menu.run()
```

### Method Chaining

Build menus fluently using method chaining:

```python
from zmenu import Menu

def view_stats():
    print("Viewing statistics...")

def export_data():
    print("Exporting data...")

settings_menu = Menu("Settings")
settings_menu.add_action("Option 1", lambda: print("Option selected"))

menu = (Menu("Dashboard")
    .add_action("View Stats", view_stats)
    .add_action("Export Data", export_data)
    .add_submenu("Settings", settings_menu))

menu.run()
```

### Deeply Nested Menus

Create hierarchies at any depth:

```python
def generate_report():
    print("Generating report...")

# Level 3
reports = Menu("Reports").add_action("Generate", generate_report)

# Level 2
data_menu = Menu("Data Management").add_submenu("Reports", reports)

# Level 1
settings = Menu("Settings").add_submenu("Data", data_menu)

# Level 0 (Main)
main = Menu("Application").add_submenu("Settings", settings)

main.run()
```

## API Reference

### Menu Class

#### Constructor

```python
Menu(title: str, items: List[MenuItem] = None, parent: Menu = None)
```

- `title`: The title displayed at the top of the menu
- `items`: Optional list of MenuItem objects
- `parent`: Optional parent menu for navigation

#### Methods

- `add_item(item: MenuItem) -> Menu`: Add a MenuItem to the menu
- `add_action(title: str, action: Callable, description: str = "") -> Menu`: Add an action item
- `add_submenu(title: str, submenu: Menu, description: str = "") -> Menu`: Add a submenu
- `run()`: Start the menu loop
- `exit()`: Exit the menu and propagate to parent menus
- `display()`: Display the menu (called automatically by run)
- `get_choice() -> int`: Get user input (called automatically by run)

### MenuItem Class

#### Constructor

```python
MenuItem(title: str, action: Callable = None, submenu: Menu = None, description: str = "")
```

- `title`: The display text for the menu item
- `action`: A callable to execute when selected (mutually exclusive with submenu)
- `submenu`: A submenu to navigate to when selected (mutually exclusive with action)
- `description`: Optional description text

#### Methods

- `execute() -> Menu | None`: Execute the item's action or return its submenu

## Examples

The `examples` directory contains sample applications:

- `simple_menu.py`: Basic menu with actions
- `nested_menus.py`: Complex nested menu structure demonstrating multiple depth levels

Run an example:

```bash
cd examples
python simple_menu.py
```

## Testing

Run the test suite:

```bash
python -m unittest discover tests
```

## Requirements

- Python 3.6 or higher

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.