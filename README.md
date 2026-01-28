# ZMenu - Multi-Level Menu Console Application

A flexible and reusable Python framework for building interactive console applications with nested menu support at unlimited depth levels.

## 📋 Overview

ZMenu is a modern console application framework that simplifies the creation of complex, hierarchical menu-driven applications. It handles all the tedious work of menu navigation, input processing, and state management, allowing developers to focus on implementing their application logic.

## ✨ Features

- **Multi-level nested menus** - Support for unlimited menu depth
- **Interactive keyboard navigation** - Arrow keys and number input support
- **Cross-platform compatibility** - Windows (MSVCRT) and Unix/Linux support
- **Clean, elegant UI** - Formatted headers, visual indicators, and status messages
- **Easy to extend** - Simple API for adding menu items and submenus
- **Automatic navigation** - Built-in "Back" option for returning to parent menus
- **Input validation** - Error handling and input validation included
- **Callable actions** - Execute any Python function when a menu item is selected
- **Visual feedback** - Highlighting for selected menu items with arrow indicators

## 📁 Project Structure

```
zmenu/
├── menu_system.py          # Core framework - Menu, MenuItem, ConsoleApp classes
├── main.py                 # Example application demonstrating all features
├── .gitignore              # Git ignore file for Python projects
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- No external dependencies required

### Running the Example Application

```bash
python main.py
```

## 🎮 Navigation Guide

| Control | Action |
|---------|--------|
| **Arrow Keys ↑ ↓** | Move between menu items |
| **Number Keys (1-9)** | Jump directly to a menu item |
| **Enter** | Select the highlighted menu item |
| **0** | Exit the application or return to parent menu |

## 📊 Example Application Structure

The included example demonstrates a complete application with multiple levels:

```
My Console Application
├── 👋 Say Hello
├── 👤 Greet User
├── 🛠️  Tools
│   ├── Calculator
│   └── System Information
├── ⚙️  Settings
│   ├── Display Options
│   │   ├── Change Theme
│   │   └── Change Font Size
│   └── Language
│       ├── English
│       ├── Español
│       └── Français
└── ❓ Help
    ├── About
    ├── How to Use
    └── Keyboard Shortcuts
```

## 📖 API Reference

### `ConsoleApp` - Main Application Class

```python
from menu_system import ConsoleApp

app = ConsoleApp("My Application Title")
main_menu = app.get_menu()  # Get the root menu
app.run()  # Start the application
```

### `Menu.add_item(key, label, action)`

Add an action item to the menu.

```python
def greet():
    print("Hello!")
    return True

menu.add_item("greet", "👋 Say Hello", greet)
```

**Parameters:**
- `key` (str): Unique identifier for the item
- `label` (str): Display text in the menu
- `action` (callable): Function to execute when selected

### `Menu.add_submenu(key, label)`

Add a submenu and return it for configuration.

```python
tools_menu = menu.add_submenu("tools", "🛠️  Tools")
tools_menu.add_item("calc", "Calculator", show_calculator)
```

**Parameters:**
- `key` (str): Unique identifier for the submenu
- `label` (str): Display text in the menu

**Returns:**
- A new `Menu` object ready for configuration

### `MenuItem` - Individual Menu Item

```python
item = MenuItem("Greet", lambda: print("Hello!"))
item.execute()  # Output: Hello!
```

## 🛠️ Creating Your Own Application

### Basic Example

```python
from menu_system import ConsoleApp

def on_action_1():
    print("You selected Action 1!")
    return True

def on_action_2():
    print("You selected Action 2!")
    return True

# Create application
app = ConsoleApp("My App")
menu = app.get_menu()

# Add menu items
menu.add_item("action1", "Action 1", on_action_1)
menu.add_item("action2", "Action 2", on_action_2)

# Add a submenu
submenu = menu.add_submenu("settings", "⚙️ Settings")
submenu.add_item("opt1", "Option 1", lambda: print("Option 1 selected"))

# Run the application
app.run()
```

### Key Guidelines

- **Return `True`** from action functions to keep the menu open
- **Return `False`** to exit the application
- Use **lambda functions** for simple, one-line actions
- Use **emoji** in labels for visual appeal (e.g., 👋, 🛠️, ⚙️, ❓)
- **Nested submenus** work at any depth level

### Advanced Example - Multi-Level Settings

```python
from menu_system import ConsoleApp

app = ConsoleApp("Settings App")
menu = app.get_menu()

# Create Settings submenu
settings = menu.add_submenu("settings", "⚙️ Settings")

# Add nested Display submenu
display = settings.add_submenu("display", "Display")
display.add_item("theme", "Change Theme", lambda: print("Theme changed"))
display.add_item("size", "Font Size", lambda: print("Font size adjusted"))

# Add nested Audio submenu
audio = settings.add_submenu("audio", "Audio")
audio.add_item("vol", "Volume", lambda: print("Volume adjusted"))
audio.add_item("mute", "Mute", lambda: print("Toggled mute"))

app.run()
```

## 💾 Action Function Best Practices

### Simple Action
```python
def simple_action():
    print("Action executed!")
    return True  # Continue menu

menu.add_item("simple", "Simple Action", simple_action)
```

### Action with User Input
```python
def action_with_input():
    try:
        name = input("Enter your name: ")
        print(f"Hello, {name}!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return True  # Stay in menu

menu.add_item("greet", "Greet User", action_with_input)
```

### Action with Data Processing
```python
def calculate():
    try:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        result = a + b
        print(f"Sum: {result}")
        return True
    except ValueError:
        print("Please enter valid numbers")
        return True

menu.add_item("calc", "Add Numbers", calculate)
```

## 🏗️ Technical Architecture

### Core Classes

**MenuItem**
- Represents a single menu item
- Stores label and optional action callable
- `execute()` method runs the associated action

**Menu**
- Manages a collection of menu items and submenus
- Handles display formatting and layout
- Processes user input (keyboard and number)
- Maintains parent-child relationships for hierarchy

**ConsoleApp**
- Top-level application controller
- Manages the root menu
- Provides `run()` method to start the application loop

### Input Processing Flow

```
User Input (keyboard or number)
    ↓
Validate input (is it a valid choice?)
    ↓
Execute action or navigate submenu
    ↓
Display result
    ↓
Redraw menu (or close if exit)
```

## 🎨 Customization Tips

### Use Emojis for Visual Appeal
```python
menu.add_item("calc", "🧮 Calculator", show_calculator)
menu.add_item("info", "ℹ️ System Info", show_system_info)
menu.add_item("gear", "⚙️ Settings", show_settings)
```

### Organize Related Options
Group related menu items in submenus for better UX:
```python
tools = menu.add_submenu("tools", "🛠️ Tools")
tools.add_item("calc", "Calculator", calculator)
tools.add_item("conv", "Converter", converter)
```

### Handle Exceptions Gracefully
Always wrap user input in try-except blocks to prevent crashes.

### Test Navigation Thoroughly
Verify that:
- All menu items are accessible
- Back/exit options work at all levels
- No infinite loops or dead ends exist

## 📋 Features Implemented

✅ Multi-level menu support (unlimited depth)
✅ Interactive keyboard navigation
✅ Number-based direct selection
✅ Automatic "Back" option in submenus
✅ Clean, formatted console output
✅ Error handling and input validation
✅ Cross-platform support
✅ Visual indicators (arrows, highlighting)
✅ Easy extensibility
✅ Built-in example application

## 🔧 Extending the Framework

### Adding a New Display Style
Modify the display methods in the `Menu` class to customize appearance.

### Custom Input Handling
Override `_get_user_choice()` to implement custom input mechanisms.

### Adding Themes
Store theme preferences and apply them in the display methods.

### Menu Persistence
Save selected options and automatically restore them on restart.

## 📝 Example Use Cases

- **System Administration Tools** - Navigate configuration options hierarchically
- **Data Entry Forms** - Multi-step menu-driven data collection
- **Game Menus** - Main menu → New Game/Load Game → Difficulty → etc.
- **CLI Tools** - Command organization in logical menu structure
- **Educational Tools** - Interactive tutorials with nested modules
- **Configuration Utilities** - Settings organized by category

## 🐛 Troubleshooting

**Q: Menu items not displaying correctly?**
- A: Check terminal width and adjust if using very small terminal

**Q: Keyboard navigation not working?**
- A: Ensure you're using a compatible terminal; MSVCRT works on Windows, Curses on Unix/Linux

**Q: Action function not executing?**
- A: Verify function returns `True` or `False` and doesn't raise unhandled exceptions

**Q: Back option appearing at wrong level?**
- A: Normal behavior - "Back" only shows in submenus, not at root level

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

Enhancements welcome:
1. Add new menu items following existing patterns
2. Create modular action functions
3. Test navigation thoroughly
4. Document new features
5. Submit improvements

---

**Happy menu building! 🎉**
