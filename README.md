# ZMenu - Interactive Console Application Framework

A Python framework for building interactive console applications with nested menus, JSON configuration, and form processing.

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)](./CHANGELOG.md)

## Features

- **JSON-based menus** - Hierarchical menu structure from `menu_config.json`
- **Minimal decorators** - `@MenuItemCmd("cmd")` with all metadata in JSON
- **Keyboard navigation** - Arrow keys, Enter, ESC, number keys
- **Unified form system** - `before_input_*` and `after_input_*` handlers
- **Cross-platform** - Works on Windows, Linux, macOS
- **Professional UI** - Colored output, emoji support, dynamic updates

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
├── input_handler.py       # Cross-platform keyboard input
├── menu_system.py         # Menu framework
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
    def hello(self):
        print("\nHello!")
        return True
    
    @MenuItemCmd("calc")
    def calc(self):
        print(f"\n2+2={2+2}")
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

### `@MenuItemCmd(cmd)`

Simple decorator for menu actions:

```python
@MenuItemCmd("hello")
def hello(self):
    return True  # Keep menu open
```

Return `False` to exit the application.

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
