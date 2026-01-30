# ZMenu - Multi-Level Menu Console Application

A flexible and reusable Python framework for building interactive console applications with nested menu support at unlimited depth levels. Features decorator-based menu item registration, cross-platform keyboard support, and automatic hierarchy management.

## 📋 Overview

ZMenu is a modern console application framework that simplifies the creation of complex, hierarchical menu-driven applications. It handles all the tedious work of menu navigation, input processing, and state management, allowing developers to focus on implementing their application logic.

## ✨ Features

- **Multi-level nested menus** - Support for unlimited menu depth with automatic hierarchy
- **Decorator-based registration** - `@MenuItemCmd` decorators for clean menu item definition
- **Interactive keyboard navigation** - Arrow keys (↑↓) with automatic menu item updates
- **Yes/No Selection** - Left/Right arrow keys with real-time updates for boolean choices
- **Multi-Select Checkboxes** - Up/Down arrow keys with Space to toggle, for multiple selections
- **Long descriptions** - Display inline descriptions when navigating to menu items
- **Cross-platform compatibility** - Windows (MSVCRT) and Unix/Linux (termios) native support
- **Smart ESC handling** - Single ESC press exits menu instantly; arrow key sequences work reliably
- **Group-based organization** - Automatic submenu creation with dot-notation grouping (e.g., "Settings.Display")
- **Custom group icons** - Map group paths to custom icons and display names
- **Visual feedback** - Formatted headers, colored selection indicators, and status messages
- **Clean, elegant UI** - Centered alignment, emoji support, consistent spacing
- **Error handling** - Input validation and graceful exception handling
- **Callable actions** - Execute any Python function when a menu item is selected
- **Automatic "Back" option** - Seamless navigation to parent menus

## 📁 Project Structure

```
zmenu/
├── menu_system.py          # Core framework - Menu, MenuItem, MenuItemCmd, ConsoleApp classes
├── console_app.py          # Application logic - Menu item definitions and group configuration
├── main.py                 # Entry point - Application initialization and setup
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
| **Arrow Keys ↑ ↓** | Move between menu items (0.5s timeout for arrow key sequences) |
| **Number Keys (1-9)** | Jump directly to a menu item |
| **Enter** | Select the highlighted menu item |
| **ESC** | Return to parent menu (or exit if at root) |
| **Ctrl+C** | Force exit from any menu |

## 🏗️ Architecture

### File Organization

**menu_system.py** - Core Framework
- `MenuItemCmd` - Decorator class for menu item metadata
- `MenuItem` - Individual menu item container
- `Menu` - Menu management with display and navigation
- `ConsoleApp` - Application controller

**console_app.py** - Application Definition
- `ConsoleApp` - Extended with `MENU_GROUP_ICONS` configuration
- `@MenuItemCmd` decorated action functions
- Group-based menu organization

**main.py** - Entry Point
- Auto-discovers decorated functions
- Registers menu items with hierarchy support
- Applies group icons
- Starts the application

### Demo Menu Hierarchy Structure

```
Root Menu (main)
├── 👋 Say Hello (immediate action)
├── 👤 Greet User (immediate action)
├── 🧮 Tools (submenu - group="Tools")
│   ├── 🧮 Calculator
│   └── ℹ️ System Information
├── 📺 Settings (submenu - group="Settings")
│   ├── Display Options (submenu - group="Settings.Display")
│   ├── Language (submenu - group="Settings.Language")
│   │   ├── English
│   │   ├── Español
│   │   └── Français
├── 📖 Help (submenu - group="Help")
│   ├── About
│   └── How to Use
└── 🕐 Show Time (immediate action)
```

## 📖 API Reference

### `@MenuItemCmd` - Menu Item Decorator

Define a menu item with metadata:

```python
@MenuItemCmd(
    cmd="unique_key",           # Required: unique identifier
    desc="Display Label",        # Required: menu label text
    order=0,                     # Optional: display order (lower first)
    label="Custom Label",        # Optional: override desc
    group="GroupName",           # Optional: submenu group (dot-notation supported)
    icon="🎯"                    # Optional: icon emoji
)
def action_function():
    # Action code
    return True  # True to keep menu open, False to exit app
```

### `Menu.add_item(key, label, action, icon=None)`

Manually add an action item to the menu:

```python
def greet():
    print("Hello!")
    return True

menu.add_item("greet", "👋 Say Hello", greet, icon="👋")
```

**Parameters:**
- `key` (str): Unique identifier for the item
- `label` (str): Display text in the menu
- `action` (callable): Function to execute when selected
- `icon` (str, optional): Icon emoji prefix

### `Menu.add_submenu(key, label, icon=None)`

Manually add a submenu:

```python
tools_menu = menu.add_submenu("tools", "Tools", icon="🛠️")
tools_menu.add_item("calc", "Calculator", show_calculator)
```

**Parameters:**
- `key` (str): Unique identifier for the submenu
- `label` (str): Display text in the menu
- `icon` (str, optional): Icon emoji prefix

**Returns:**
- A new `Menu` object ready for configuration

### `Menu.register(*functions)`

Register all decorated menu item functions:

```python
# Import decorated functions
from console_app import hello_world, show_calculator

menu.register(hello_world, show_calculator)
```

This method:
- Scans for `@MenuItemCmd` decorators
- Sorts by order
- Creates submenus based on `group` parameter
- Applies group icons if configured

### `ConsoleApp` - Application Controller

```python
app = ConsoleApp("Application Title")
menu = app.get_menu()
menu.register(*decorated_functions)
app.run()
```

## 💻 Creating Your Own Application

### Step 1: Define Actions with Decorators

```python
# In console_app.py

@MenuItemCmd("exit_app", "Exit", order=99, icon="❌")
def exit_app():
    print("Goodbye!")
    return False  # Return False to exit

@MenuItemCmd("tool1", "Tool 1", order=0, group="Tools", icon="🔧")
def use_tool1():
    print("Tool 1 executing...")
    return True

@MenuItemCmd("opt1", "Option 1", order=0, group="Settings", icon="⚙️")
def set_option1():
    print("Setting option 1...")
    return True
```

### Step 2: Configure Group Icons

```python
class ConsoleApp:
    MENU_GROUP_ICONS = {
        "Tools":        ("🛠️", "Tools"),
        "Settings":     ("⚙️", "Settings"),
        "Tools.Advanced": ("🔬", "Advanced Tools")
    }
```

Format: `"group_path": (icon_emoji, display_name)`

### Step 3: Auto-Register in main.py

```python
import inspect
from console_app import ConsoleApp, *  # Import all decorated functions

app = ConsoleApp("My App")
menu = app.get_menu()

# Auto-discover decorated functions
decorated = [fn for name, fn in inspect.getmembers(console_app, 
             predicate=inspect.isfunction) if hasattr(fn, 'cmd')]
menu.register(*decorated)

app.run()
```

## 🔑 Key Concepts

### Order Parameter
Controls display sequence (lower numbers appear first):
```python
@MenuItemCmd("first", "First Item", order=1)
@MenuItemCmd("second", "Second Item", order=2)
@MenuItemCmd("third", "Third Item", order=3)
```

### Group Parameter
Creates hierarchical submenus using dot notation:
```python
@MenuItemCmd("display", "Display", group="Settings")           # Submenu of Settings
@MenuItemCmd("theme", "Theme", group="Settings.Display")       # Sub-submenu
@MenuItemCmd("darkmode", "Dark Mode", group="Settings.Display") # Same level as theme
```

### Return Values
- **`True`** - Keep menu open (wait for next user action)
- **`False`** - Exit application immediately

### Icon Usage
- Use emoji for visual appeal: 👋, 🛠️, ⚙️, 📖, ❓
- Icons are automatically prefixed to labels
- Group icons override item icons

## 🎯 Best Practices

### 1. Use Decorators for All Menu Items
```python
@MenuItemCmd("key", "Label", order=0)
def my_action():
    return True
```

### 2. Organize with Groups
```python
@MenuItemCmd("a", "Item A", group="Category")
@MenuItemCmd("b", "Item B", group="Category")
```

### 3. Handle Errors Gracefully
```python
@MenuItemCmd("user_input", "Get Input")
def get_user_input():
    try:
        value = input("Enter value: ")
        # Process value
        return True
    except Exception as e:
        print(f"Error: {e}")
        return True  # Stay in menu
```

### 4. Use Consistent Ordering
```python
# Root level
@MenuItemCmd("a", "First", order=1)
@MenuItemCmd("b", "Second", order=2)
@MenuItemCmd("c", "Exit", order=99)

# In groups
@MenuItemCmd("x", "Item X", group="Tools", order=1)
@MenuItemCmd("y", "Item Y", group="Tools", order=2)
```

## 🎯 Interactive Prompts

### Yes/No Selection

Display a boolean choice with left/right arrow navigation:

```python
result = menu.yes_no_prompt(
    question="Do you want to continue?",
    description="Use LEFT/RIGHT arrow keys to select"
)

if result is True:
    print("User selected: YES")
elif result is False:
    print("User selected: NO")
else:
    print("User cancelled (Escape)")
```

**Navigation:**
- **Left/Right Arrows**: Switch between YES and NO
- **Enter**: Confirm selection
- **Escape**: Cancel

### Multi-Select Checkboxes

Display a list of items with checkbox selection:

```python
items = [
    {"label": "Option 1", "description": "First choice", "selected": False},
    {"label": "Option 2", "description": "Second choice", "selected": True},
    {"label": "Option 3", "description": "Third choice", "selected": False},
]

selected = menu.multi_select_prompt("Select items:", items)

if selected is None:
    print("Selection cancelled")
else:
    for item in selected:
        print(f"Selected: {item['label']}")
```

**Navigation:**
- **Up/Down Arrows**: Navigate items
- **Space**: Toggle checkbox for current item
- **Enter**: Confirm selection
- **Escape**: Cancel

## 📝 Example Use Cases

- **System Administration Tools** - Configuration management with nested menus
- **Interactive CLI Tools** - Command-line interfaces with hierarchical commands
- **Game Menus** - Main menu → Game → Settings → Audio/Video
- **Data Entry Forms** - Multi-step menu-driven data collection with confirmations
- **Package/Dependency Management** - Multi-select with yes/no confirmations
- **Educational Tools** - Interactive tutorials with modular content
- **DevOps Tools** - Infrastructure management with grouped operations

---

**Happy menu building! 🎉**
