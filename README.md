# ZMenu - Interactive Console Application Framework

A powerful and flexible Python framework for building interactive console applications with unlimited nested menu levels, JSON-based configuration, and a revolutionary **dual-mode form system**.

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com)
[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)](./CHANGELOG.md)

---

## 🎯 Overview

ZMenu simplifies building sophisticated console applications with:
- **Unlimited menu nesting** - Organize complex hierarchies effortlessly
- **JSON-based configuration** - Centralized menu structure, easy to maintain and customize
- **Decorator-based actions** - Clean, minimal `@MenuItemCmd` decorator syntax
- **Interactive form system** - Three powerful modes for form processing
- **Cross-platform support** - Windows and Unix/Linux/macOS compatibility
- **Professional UI** - Beautiful, user-friendly console interface with hierarchical display

Perfect for CLI tools, system utilities, admin dashboards, and interactive applications.

## ✨ Features

- **JSON-driven menu hierarchy** - Define menus in `menu_config.json` with unlimited nesting
- **Hierarchical structure** - Menu items follow display order from JSON configuration
- **Minimal decorators** - `@MenuItemCmd` only needs command identifier (cmd parameter)
- **Interactive keyboard navigation** - Arrow keys (↑↓) with automatic menu item updates
- **Yes/No Selection** - Left/Right arrow keys with real-time updates for boolean choices
- **Multi-Select Checkboxes** - Up/Down arrow keys with Space to toggle, for multiple selections
- **Field descriptions** - Display inline descriptions (desc) when navigating menu items
- **Cross-platform compatibility** - Unified input handling for Windows (MSVCRT) and Unix/Linux (termios)
- **Smart ESC handling** - Single ESC press exits menu instantly; arrow key sequences work reliably
- **Semantic field naming** - label (display text), desc (description), icon (emoji), cmd (command)
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
├── menu_config.json        # Hierarchical menu structure (JSON) - CENTRALIZED CONFIG
├── input_handler.py        # Unified cross-platform keyboard input handling
├── ansi_manager.py         # ANSI color scheme management
├── menu_system.py          # Core framework - Menu, MenuItem, MenuItemCmd classes
├── form_system.py          # Form system - Interactive, Submit, and Pre-validation modes
├── console_app.py          # Application logic - Menu item action methods
├── main.py                 # Entry point - Application initialization
├── form_example.json       # Sample form definition for demos
└── README.md               # This file
```

### Architecture Highlights

**menu_config.json** - JSON-based hierarchical menu structure
```json
{
  "menu": [
    {
      "cmd": "greeting",
      "label": "Say Hello",
      "icon": "👋",
      "desc": "Display a friendly greeting message"
    },
    {
      "name": "Tools",
      "icon": "🛠️",
      "desc": "Collection of utility tools",
      "items": [
        {"cmd": "calc", "label": "Calculator", "icon": "🧮", "desc": "..."}
      ]
    }
  ]
}
```

**input_handler.py** - Centralized cross-platform input
- Unified keyboard handling for Windows (msvcrt) and Unix (termios)
- Returns simple strings: 'up', 'down', 'left', 'right', 'enter', 'esc'
- Handles platform-specific code in one place

**Decorator Pattern** - Minimal and clean
```python
@MenuItemCmd("cmd_name")
def action_method(self):
    return True
```
All metadata (label, desc, icon, display order) loaded from menu_config.json

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- No external dependencies required

### Running the Example Application

```bash
python main.py
```

### Creating a Custom Application

#### Step 1: Define Your Menu Structure (menu_config.json)

```json
{
  "menu": [
    {
      "cmd": "hello",
      "label": "Say Hello",
      "icon": "👋",
      "desc": "Display a greeting"
    },
    {
      "name": "Tools",
      "icon": "🛠️",
      "desc": "Utility tools",
      "items": [
        {
          "cmd": "calc",
          "label": "Calculator",
          "icon": "🧮",
          "desc": "Basic arithmetic"
        }
      ]
    }
  ]
}
```

#### Step 2: Implement Action Methods (console_app.py)

```python
from menu_system import MenuItemCmd

class ConsoleApp:
    @MenuItemCmd("hello")
    def hello_world(self):
        print("\n👋 Hello from the console app!")
        return True

    @MenuItemCmd("calc")
    def show_calculator(self):
        num1 = float(input("\nEnter first number: "))
        num2 = float(input("Enter second number: "))
        print(f"\n  {num1} + {num2} = {num1 + num2}")
        return True
```

#### Step 3: Initialize and Run (main.py)

```python
from console_app import ConsoleApp

app = ConsoleApp("My App")
app.run()
```

The framework automatically:
1. Discovers decorated methods
2. Loads JSON configuration
3. Matches cmd values to methods
4. Builds the menu hierarchy
5. Displays and manages the menu

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

### JSON-Based Configuration (menu_config.json)

The menu structure is now completely defined in JSON with hierarchical organization:

```json
{
  "menu": [
    {
      "cmd": "greeting",           # Command ID (links to @MenuItemCmd)
      "label": "Say Hello",        # Display label in menu
      "icon": "👋",               # Icon emoji (optional)
      "desc": "Description text"   # Item description
    },
    {
      "name": "Tools",             # Submenu group name
      "icon": "🛠️",
      "desc": "Group description",
      "items": [                   # Nested items
        {"cmd": "calc", "label": "Calculator", ...},
        {"cmd": "sysinfo", "label": "System Info", ...}
      ]
    }
  ]
}
```

**Key Principles:**
- Menu order follows JSON array order (no sorting logic needed)
- Supports unlimited nesting levels
- All metadata centralized and easy to maintain
- Icons optional (will be omitted if not specified)

### Input Handler (input_handler.py)

Unified cross-platform keyboard input handling:
- **Windows**: Uses `msvcrt` module
- **Unix/Linux/macOS**: Uses `termios` and `fcntl`
- **Interface**: Returns simple strings like 'up', 'down', 'enter', 'esc'

### Decorator Pattern (console_app.py)

Simplified decorator with only command parameter:

```python
@MenuItemCmd("cmd_name")  # Only parameter needed!
def action_method(self):
    """Action implementation"""
    return True
```

**How it works:**
1. Decorator stores `cmd` attribute on method
2. `setup_menu()` collects all decorated methods
3. `register()` loads JSON config and matches cmd values
4. Action methods are passed to menu registration

### Core Registration Flow

```
menu.register(*decorated_methods, config_path="menu_config.json")
  ↓
1. Load JSON config (hierarchical structure)
2. Recursively process items and submenus
3. Match @MenuItemCmd decorated methods by cmd value
4. Add items/submenus to Menu object
5. Display order = JSON array order (no sorting!)
```

## 📖 API Reference

### Configuration Fields (menu_config.json)

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| **cmd** | string | For actions | Command identifier (links to @MenuItemCmd) |
| **label** | string | Yes | Display text for menu item |
| **name** | string | For submenus | Display name for submenu group |
| **icon** | string | No | Emoji icon (optional) |
| **desc** | string | No | Item description/help text |
| **items** | array | For submenus | Array of nested items |

### `@MenuItemCmd` - Minimal Decorator

Define a menu action with only the command identifier:

```python
@MenuItemCmd("cmd_name")
def action_method(self):
    """Implementation"""
    return True
```

**Parameters:**
- `cmd` (str): Unique command identifier (must match `cmd` in menu_config.json)

**Return Values:**
- `True` - Keep menu open, wait for next action
- `False` - Exit application immediately

**Note:** All other metadata (label, desc, icon) comes from menu_config.json

### `Menu.register(*functions, config_path=None)`

Register decorated action methods and load hierarchical menu structure:

```python
# Collect decorated methods
decorated_methods = []
for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
    if hasattr(method, 'cmd'):
        decorated_methods.append(method)

# Register with JSON configuration
menu.register(*decorated_methods, config_path='menu_config.json')
```

**Process:**
1. Loads menu_config.json from specified path
2. Recursively processes hierarchical structure
3. Matches cmd values to decorated methods
4. Builds menu following JSON array order
5. No sorting needed - JSON order is authoritative

### `Menu.add_item(cmd, label, action, icon=None, desc=None)`

Manually add an action item to the menu:

```python
def greet():
    print("Hello!")
    return True

menu.add_item("greet", "Say Hello", greet, icon="👋", desc="Greeting demo")
```

**Parameters:**
- `cmd` (str): Unique identifier for the item
- `label` (str): Display text in the menu
- `action` (callable): Function to execute when selected
- `icon` (str, optional): Icon emoji prefix
- `desc` (str, optional): Description text

### `Menu.add_submenu(name, label, icon=None, desc=None)`

Manually add a submenu:

```python
tools_menu = menu.add_submenu("tools", "Tools", icon="🛠️", desc="Utility tools")
tools_menu.add_item("calc", "Calculator", show_calculator)
```

**Parameters:**
- `name` (str): Unique identifier for the submenu
- `label` (str): Display text in the menu
- `icon` (str, optional): Icon emoji prefix
- `desc` (str, optional): Submenu description

**Returns:**
- A new `Menu` object ready for configuration

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

### JSON Hierarchy Rules

1. **Root items** - Direct children of `"menu"` array
2. **Submenus** - Items with `"name"` and `"items"` properties
3. **Actions** - Items with `"cmd"` property
4. **Display order** - Follows JSON array order (no sorting needed)
5. **Unlimited nesting** - Each submenu can have submenus

Example:
```json
{
  "menu": [
    {"cmd": "action1", "label": "Action 1"},     // Direct action
    {
      "name": "Group",
      "items": [
        {"cmd": "action2", "label": "Action 2"},  // Submenu action
        {
          "name": "Subgroup",
          "items": [
            {"cmd": "action3", "label": "Action 3"} // Nested action
          ]
        }
      ]
    }
  ]
}
```

### Field Naming Clarity

| Field | Purpose | Example |
|-------|---------|---------|
| **cmd** | Command identifier | `"greeting"` |
| **label** | Display text | `"Say Hello"` |
| **desc** | Description/help | `"Display a greeting message"` |
| **icon** | Visual emoji | `"👋"` |
| **name** | Submenu group name | `"Tools"` |
| **items** | Child menu items | `[{...}, {...}]` |

### Return Values in Actions

```python
@MenuItemCmd("my_action")
def my_action(self):
    # ... do something ...
    return True   # Keep menu open
    # return False  # Exit application
```

### Error Handling

```python
@MenuItemCmd("risky_action")
def risky_action(self):
    try:
        # Perform action
        result = dangerous_operation()
        return True  # Keep menu open on success
    except Exception as e:
        print(f"❌ Error: {e}")
        return True  # Keep menu open on error
```

## 🎯 Best Practices

### 1. Structure Your menu_config.json Logically

```json
{
  "menu": [
    {"cmd": "main_action", "label": "Main Action"},
    {
      "name": "Utilities",
      "icon": "🛠️",
      "items": [
        {"cmd": "util1", "label": "Utility 1"},
        {"cmd": "util2", "label": "Utility 2"}
      ]
    },
    {"cmd": "exit", "label": "Exit"}
  ]
}
```

### 2. Keep Decorators Minimal

```python
# Good ✓
@MenuItemCmd("my_action")
def my_action(self):
    return True

# Avoid ✗ (use JSON instead)
# @MenuItemCmd("my_action", label="...", desc="...", icon="...", order=1)
```

### 3. Use Descriptive Labels and Descriptions

```json
{
  "cmd": "backup",
  "label": "Create Backup",
  "desc": "Backup all user data to external drive",
  "icon": "💾"
}
```

### 4. Organize Menus Hierarchically

```json
{
  "name": "Settings",
  "items": [
    {
      "name": "Display",
      "items": [
        {"cmd": "theme", "label": "Theme"},
        {"cmd": "font", "label": "Font Size"}
      ]
    },
    {
      "name": "Language",
      "items": [
        {"cmd": "en", "label": "English"},
        {"cmd": "es", "label": "Español"}
      ]
    }
  ]
}
```

### 5. Handle Errors Gracefully

```python
@MenuItemCmd("user_input")
def get_user_input(self):
    try:
        value = input("Enter value: ")
        self.process_value(value)
        print("✓ Value processed successfully")
        return True
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
        return True  # Stay in menu to retry
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return True
```

### 6. Use Icons Consistently

```json
{
  "menu": [
    {"cmd": "info", "label": "Information", "icon": "ℹ️"},
    {"cmd": "settings", "label": "Settings", "icon": "⚙️"},
    {"cmd": "tools", "label": "Tools", "icon": "🛠️"},
    {"cmd": "help", "label": "Help", "icon": "❓"},
    {"cmd": "exit", "label": "Exit", "icon": "❌"}
  ]
}
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
