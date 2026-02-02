# ZMenu - Interactive Console Application Framework

A powerful and flexible Python framework for building interactive console applications with unlimited nested menu levels, decorator-based registration, and a revolutionary **dual-mode form system**.

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](./CHANGELOG.md)

---

## 🎯 Overview

ZMenu simplifies building sophisticated console applications with:
- **Unlimited menu nesting** - Organize complex hierarchies effortlessly
- **Decorator-based menu items** - Clean, Pythonic syntax with `@MenuItemCmd`
- **Interactive form system** - Two powerful modes for form processing
- **Cross-platform support** - Windows and Unix/Linux/macOS compatibility
- **Professional UI** - Beautiful, user-friendly console interface

Perfect for CLI tools, system utilities, admin dashboards, and interactive applications.

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

## 📝 Form System (NEW - v2.0)

**Dual-mode form system** with three powerful approaches:

### Interactive Mode 🔄
- Process each field with immediate callbacks
- Real-time validation and data transformation
- Perfect for complex workflows and database operations
- Handler pattern: `on_field_<field_id>(value, field)`

### Pre-Validation Mode 🔄 (NEW!)
- Check for existing values before prompting user input
- Suggest default values based on previously stored data
- Allow users to confirm or override existing values
- Handler pattern: `pre_validate_<field_id>(field, current_results)`

### Submit Mode 📤
- Batch collection and unified submission
- Automatic API endpoint integration
- Perfect for REST APIs and simple submissions
- Clean, atomic validation

**See:** [KEYBOARD_CONTROLS.md](KEYBOARD_CONTROLS.md) - Keyboard controls and interaction guide

## 📁 Project Structure

```
zmenu/
├── menu_system.py          # Core framework - Menu, MenuItem, MenuItemCmd classes
├── form_system.py          # Form system - Interactive, Submit, and Pre-validation modes
├── console_app.py          # Application logic - Menu item definitions and form handlers
├── main.py                 # Entry point - Application initialization and setup
├── form_example.json       # Sample form definition for demos
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

## ⌨️ Keyboard Controls in Forms

ZMenu provides intuitive keyboard controls for form interactions:

### Choice Fields (Single/Multi Selection)

| Control | Action |
|---------|--------|
| **↑ ↓ Arrow Keys** | Navigate between options |
| **← → Arrow Keys** | Navigate between options (alternative to ↑ ↓) |
| **Enter** | Confirm selection and proceed |
| **ESC** | Cancel selection |
| **Space** | Toggle selection (multi-choice only) |
| **Other Keys** | Ignored (no interface refresh) |

**Important:** Invalid keys (letters, numbers, etc.) are silently ignored and do not cause interface refresh, ensuring smooth user experience.

### Text Input Fields

| Control | Action |
|---------|--------|
| **Type normally** | Enter text as usual |
| **Enter** | Submit text input |
| **Backspace/Delete** | Edit text as standard |
| **ESC** | Cancel input (when supported) |

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
├── ✅ Confirm Demo (interactive yes/no selection)
├── ☑️ Multi-Select Demo (interactive multi-select with checkboxes)
├── 🧮 Tools (submenu - group="Tools")
│   ├── 🧮 Calculator (with arithmetic operations)
│   ├── ℹ️ System Information (display system details)
│   └── 🕐 Show Time (display current date and time)
├── 📁 nLevel Menu (submenu - group="Settings")
│   ├── 📺 Display Options (submenu - group="Settings.Display")
│   │   ├── 🎨 Change Theme
│   │   └── 🔠 Change Font Size
│   └── 🌐 Language (submenu - group="Settings.Language")
│       ├── English
│       ├── Español
│       └── Français
├── 📝 Form Interactive Mode (form system in interactive mode)
├── 📤 Form Submit Mode (form system in submit mode)
└── 🔄 Form with Pre-Validation (form system with pre-validation)
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

### `FormSystem` - Form System with Three Modes

Initialize form system with flexible mode support:

```python
# Interactive mode - Process each field with callbacks
form_system = FormSystem(
    mode='interactive',
    handler=field_handler,                 # Handler with on_field_* methods
    pre_validation_handler=pre_validator   # Optional pre-validation
)

# Submit mode - Batch collection and submission
form_system = FormSystem(
    mode='submit',
    endpoint='https://api.example.com/submit'  # Optional API endpoint
)
```

### Interactive Mode Handler Pattern

Create a handler with field callback methods:

```python
class FormFieldHandler:
    def on_field_{field_id}(self, value, field):
        """
        Process field after user input.
        
        Args:
            value: User-entered value
            field: The FormField object with metadata
        """
        # Process, validate, or transform the value
        print(f"Processing {field.label}: {value}")
```

### Pre-Validation Handler Pattern

Create a handler to suggest existing values:

```python
class FormPreValidationHandler:
    def pre_validate_{field_id}(self, field, current_results):
        """
        Suggest value before user input.
        
        Args:
            field: The FormField object with metadata
            current_results: Results collected so far
            
        Returns:
            Pre-validated value or None
        """
        # Check database, cache, or previous values
        if existing_value_available:
            return existing_value
        return None
```

## � Form Examples

### Example 1: Interactive Mode with Callbacks

```python
from form_system import FormSystem

# Create handler with field callbacks
class MyFormHandler:
    def on_field_name(self, value, field):
        print(f"✓ Name processed: {value}")
    
    def on_field_email(self, value, field):
        print(f"✓ Email validated: {value}")

# Initialize and process
form = FormSystem(mode='interactive', handler=MyFormHandler())
results = form.process_form(form_definition)
```

### Example 2: Submit Mode with API Endpoint

```python
# Batch collection with automatic submission
form = FormSystem(
    mode='submit',
    endpoint='https://api.example.com/submit'
)
results = form.process_form(form_definition)
# Results automatically submitted to endpoint
```

### Example 3: Pre-Validation with Existing Data

```python
# Suggest existing values to users
class PreValidator:
    def pre_validate_email(self, field, current_results):
        # Return existing email if available
        return "user@example.com"

form = FormSystem(
    mode='interactive',
    handler=MyFormHandler(),
    pre_validation_handler=PreValidator()
)
results = form.process_form(form_definition)
```

## 📋 Form Menu Items in Demo

The example application includes three form demos:

| Menu Item | Mode | Features |
|-----------|------|----------|
| **Form Interactive Mode** | Interactive | Immediate field callbacks, real-time processing |
| **Form Submit Mode** | Submit | Batch collection, automatic file save |
| **Form with Pre-Validation** | Interactive + Pre-validation | Suggest existing values, user confirmation |

All form examples use the same `form_example.json` file but demonstrate different processing strategies.



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
