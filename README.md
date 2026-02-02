# ZMenu - Interactive Console Application Framework

A Python framework for building interactive console applications with nested menus, parameter collection, form processing, and JSON configuration.

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)](./CHANGELOG.md)

## Features

- **JSON-based menus** - Hierarchical menu structure from `menu_config.json`
- **Parameter system** - `params` (required) and `options` (optional) for menu actions
- **Minimal decorators** - `@MenuItemCmd("cmd", params=[], options=[])` configuration
- **Keyboard navigation** - Arrow keys, Enter, ESC, number keys
- **Unified form system** - Interactive form processing with field handlers
- **Cross-platform** - Works on Windows, Linux, macOS
- **Professional UI** - Colored output, emoji support, dynamic updates

## Menu Item Parameters

Menu actions support two types of parameters:

### Required Parameters (`params`)
These are collected from the user before action execution:

```python
@MenuItemCmd(
    "calc",
    params=[
        {'name': 'num1', 'type': 'number', 'description': 'First number'},
        {'name': 'num2', 'type': 'number', 'description': 'Second number'},
    ]
)
def show_calculator(self, params, options):
    num1 = float(params.get('num1', 0))
    num2 = float(params.get('num2', 0))
    return True
```

### Optional Parameters (`options`)
Collected using command-line style syntax: `--key1 value1 --key2 value2`

```python
@MenuItemCmd(
    "calc",
    options=[
        {'name': 'operation', 'type': 'choice', 'choices': ['add', 'subtract', 'multiply', 'divide']},
        {'name': 'text', 'type': 'string', 'description': 'a string text'},
    ]
)
def show_calculator(self, params, options):
    operation = options.get('operation', 'add')  # Default if not provided
    text = options.get('text', 'no value')
    return True
```

**Parameter Types:**
- `text` - Plain text input
- `number` - Numeric input (validated)
- `choice` - Single selection from list
- `string` - String input (for options only)
- `bool` - Boolean flag (for options only)

**Options Input Format:**
```
--operation multiply --text "hello world"
```

Supports quoted strings with spaces and escape sequences:
- `\"` for literal double quote
- `\\` for literal backslash

## Form System

Single, consistent handler pattern for field processing:

```python
class FormHandler:
    def before_input_<field_id>(self, field, current_results):
        """Called before user input - suggest a value or return None"""
        return existing_value or None
    
    def after_input_<field_id>(self, value, field, current_results):
        """Called after user input - process or validate"""
        print(f"Value processed: {value}")
```

**Operating Modes:**
| Mode | Purpose |
|------|---------|
| **interactive** | Process fields with `after_input_*` callbacks |
| **submit** | Batch collection, auto-submit to endpoint |
| **pre-validation** | Suggest values with `before_input_*` |

## Project Structure

```
zmenu/
├── menu_config.json       # Menu structure (JSON)
├── menu_system.py         # Menu framework & parameter collection
├── form_system.py         # Form system
├── console_app.py         # Application actions
├── main.py                # Entry point
└── README.md              # This file
```

## Quick Start

### Prerequisites
Python 3.6+, no external dependencies

### Run the Example
```bash
python main.py
```

### Create a Custom App

**1. Define menu structure in `menu_config.json`:**
```json
{
  "menu": [
    {"cmd": "hello", "label": "Say Hello"},
    {"name": "Tools", "items": [
      {"cmd": "calc", "label": "Calculator"}
    ]}
  ]
}
```

**2. Implement actions in `console_app.py`:**
```python
from menu_system import MenuItemCmd

class ConsoleApp:
    @MenuItemCmd("hello")
    def hello(self, params, options):
        print("\nHello!")
        return True
    
    @MenuItemCmd(
        "calc",
        params=[
            {'name': 'num1', 'type': 'number', 'description': 'First number'},
            {'name': 'num2', 'type': 'number', 'description': 'Second number'},
        ],
        options=[
            {'name': 'operation', 'type': 'choice', 'choices': ['add', 'subtract', 'multiply', 'divide']},
        ]
    )
    def calc(self, params, options):
        num1 = float(params.get('num1', 0))
        num2 = float(params.get('num2', 0))
        operation = options.get('operation', 'add')
        print(f"\n{num1} {operation} {num2}")
        return True
```

**3. Initialize in `main.py`:**
```python
from console_app import ConsoleApp
app = ConsoleApp("My App")
app.run()
```

## Navigation

| Key | Action |
|-----|--------|
| **Up/Down Arrows** | Navigate menu items |
| **1-9** | Jump to item number |
| **Enter** | Select item |
| **ESC** | Back/Exit |
| **Space** | Toggle (multi-select) |
| **Ctrl+C** | Force exit |

**Form Navigation:**
- **Text input:** Type normally, Enter to submit
- **Single choice:** Up/Down or Left/Right to select, Enter to confirm
- **Multi-choice:** Up/Down to navigate, Space to toggle, Enter to confirm

## Architecture

### JSON Configuration

Menu structure with hierarchical organization:

```json
{
  "menu": [
    {
      "cmd": "greeting",      # Command ID
      "label": "Say Hello",   # Display text
      "desc": "Description"   # Optional help
    },
    {
      "name": "Tools",        # Submenu group
      "items": [              # Nested items
        {"cmd": "calc", "label": "Calculator"}
      ]
    }
  ]
}
```

**Key Principles:**
- Menu order follows JSON array order
- Supports unlimited nesting
- All metadata centralized

### Decorator Pattern

Minimal decorator with metadata from JSON:

```python
@MenuItemCmd("cmd_name")  # Only command parameter!
def action_method(self):
    return True   # Keep menu open
```

## API Reference

### Configuration Fields

| Field | Required | Purpose |
|-------|----------|---------|
| **cmd** | For actions | Command ID |
| **label** | Yes | Display text |
| **name** | For submenus | Submenu name |
| **desc** | No | Help text |
| **items** | For submenus | Nested items |

### `@MenuItemCmd(cmd, params=[], options=[])`

Decorator for menu actions with optional parameter definitions:

```python
@MenuItemCmd(
    "hello",
    params=[
        {'name': 'name', 'type': 'text', 'description': 'Your name', 'validation_rule': 'required'}
    ],
    options=[
        {'name': 'greeting', 'type': 'choice', 'choices': ['Hi', 'Hello', 'Hey']}
    ]
)
def hello(self, params, options):
    name = params.get('name', '')
    greeting = options.get('greeting', 'Hello')
    print(f"{greeting}, {name}!")
    return True  # Keep menu open
```

**Parameters:**
- `cmd` (str): Unique command identifier
- `params` (list): Required parameters collected before action execution
- `options` (list): Optional parameters collected via CLI-style syntax

Return `False` to exit the application.

### Parameter Definition

**Required Parameters (`params`) Definition:**
```python
{
    'name': 'field_id',           # Unique identifier
    'type': 'text|number|choice', # Field type
    'description': 'Help text',   # Shown to user
    'validation_rule': 'required',# Optional: required, min_length:N, max_length:N, range:MIN-MAX
    'default': 'default_value'    # Optional: default value
}
```

**Optional Parameters (`options`) Definition:**
```python
{
    'name': 'field_id',                # Unique identifier
    'type': 'choice|string|bool',      # Field type (string/bool for options only)
    'description': 'Help text',        # Optional: help text
    'choices': ['option1', 'option2']  # Required for choice type
}
```

### `Menu.register(*functions, config_path="menu_config.json")`

Register decorated methods and load JSON configuration.

### `FormSystem(mode, handler=None, endpoint=None)`

Initialize the form system with one of three modes.

**Example:**
```python
form = FormSystem(mode='interactive', handler=MyHandler())
results = form.process_form(form_data)
```

## Form Examples

### Interactive Mode with Field Processing

```python
class MyHandler:
    def before_input_email(self, field, results):
        """Suggest existing email"""
        return "user@example.com"  # or None
    
    def after_input_email(self, value, field, results):
        """Validate email"""
        if '@' in value:
            print("Valid email")
```

### Pre-Validation and Processing

```python
form = FormSystem(mode='interactive', handler=MyHandler())
results = form.process_form(form_data)
```

### Submit Mode

```python
form = FormSystem(mode='submit', endpoint='https://api.example.com/submit')
results = form.process_form(form_data)
```

## Best Practices

- Keep JSON configuration organized and readable
- Use descriptive labels and descriptions
- Return `True` to keep menu open, `False` to exit
- Handle errors gracefully in action methods
- Use icons consistently across menus
- Structure forms logically with before/after handlers

---

**Happy menu building!**
