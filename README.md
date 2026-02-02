# ZMenu - Interactive Console Application Framework

A Python framework for building interactive console applications with nested menus, parameter collection, form processing, and JSON-based configuration.

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)](./CHANGELOG.md)

## Features

- **JSON-based Menu Structure** - Hierarchical menus defined in `menu_config.json`
- **Parameter Collection System**
  - `params`: Required parameters collected via form
  - `options`: Optional parameters via CLI-style syntax (`--key value`)
- **Minimal Decorators** - Simple `@MenuItemCmd` with metadata
- **Keyboard Navigation** - Arrow keys, Enter, ESC, number keys
- **Unified Form System** - Interactive form processing with field handlers
- **Cross-platform** - Windows, Linux, macOS support
- **Rich UI** - Colored output, emoji support, dynamic updates

## Project Structure

```
zmenu/
├── menu_config.json         # Menu structure in JSON
├── menu_system.py           # Menu framework & parameter collection
├── form_system.py           # Form system for data collection
├── input_handler.py         # Keyboard input handling
├── ansi_manager.py          # ANSI color and formatting
├── console_app.py           # Application actions
├── main.py                  # Entry point
└── README.md                # This file
```

## Quick Start

### Prerequisites
- Python 3.6+
- No external dependencies

### Run the Example

```bash
python main.py
```

## How It Works

### 1. Menu Structure (menu_config.json)

Define your menu hierarchy as JSON:

```json
{
  "menu": [
    {
      "cmd": "greeting",
      "label": "Say Hello",
      "icon": "👋",
      "desc": "Display a greeting"
    },
    {
      "label": "Tools",
      "icon": "🛠️",
      "items": [
        {
          "cmd": "calc",
          "label": "Calculator",
          "icon": "🧮"
        }
      ]
    }
  ]
}
```

**Menu Item Fields:**
- `cmd`: Command ID (mapped to method)
- `label`: Display text (required)
- `icon`: Unicode emoji or symbol (optional)
- `desc`: Help description (optional)
- `items`: Submenu items (for grouping)

### 2. Define Actions (console_app.py)

Implement action methods with `@MenuItemCmd` decorator:

```python
from menu_system import MenuItemCmd

class ConsoleApp:
    @MenuItemCmd("greeting")
    def hello_world(self, params, options):
        print("Hello!")
        return True  # Keep menu open
```

**Method Signature:**
- `params`: Dict with required parameters
- `options`: Dict with optional parameters
- Return `True` to keep menu open, `False` to exit

### 3. Start Application (main.py)

```python
from console_app import ConsoleApp

app = ConsoleApp("My App")
app.run()
```

## Menu Item Parameters

Menu actions support two types of parameters:

### Required Parameters (`params`)

Collected from user via interactive form before action execution:

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
    print(f"Numbers: {num1}, {num2}")
    return True
```

**Parameter Types:**
- `text` - Plain text input (for both params and options)
- `number` - Numeric input (validated)
- `choice` - Single selection from list
- `bool` - Boolean flag (for options only)

**Parameter Definition:**
```python
{
    'name': 'field_id',           # Unique identifier
    'type': 'text|number|choice', # Field type
    'description': 'Help text',   # Shown to user
    'validation_rule': 'required',# Optional: required, min_length:N, max_length:N, range:MIN-MAX
    'default': 'value'            # Optional: default value
}
```

### Optional Parameters (`options`)

Collected via command-line style syntax after params:

```python
@MenuItemCmd(
    "calc",
    options=[
        {'name': 'operation', 'type': 'choice', 'choices': ['add', 'subtract', 'multiply', 'divide']},
        {'name': 'text', 'type': 'string', 'description': 'Text note'},
    ]
)
def show_calculator(self, params, options):
    operation = options.get('operation', 'add')      # Default if not provided
    text = options.get('text', 'no value')
    return True
```

**Options Input Format:**
```
--operation multiply --text "hello world"
```

**Features:**
- Quoted strings support spaces: `"hello world"`
- Escape sequences:
  - `\"` for literal double quote
  - `\\` for literal backslash
- Boolean flags (presence = True): `--flag`

**Example with Escapes:**
```
--text "He said \"Hello\"" --path "C:\\Users\\file.txt"
```

**Options Definition:**
```python
{
    'name': 'field_id',                # Unique identifier
    'type': 'choice|string|bool',      # Field type
    'description': 'Help text',        # Optional
    'choices': ['opt1', 'opt2']        # Required for choice type
}
```

## Form System

The form system processes parameter collection with configurable modes:

### Mode: Interactive

Process fields with callbacks for custom handling:

```python
class MyHandler:
    def before_input_email(self, field, current_results):
        """Called before user input - suggest value"""
        return "user@example.com" or None
    
    def after_input_email(self, value, field, current_results):
        """Called after user input - process/validate"""
        if '@' in value:
            print("✓ Valid email")
```

### Mode: Submit

Auto-collect and submit to endpoint:

```python
form = FormSystem(mode='submit', endpoint='https://api.example.com/submit')
results = form.process_form(form_data)
```

### Mode: Pre-validation

Suggest values before input:

```python
form = FormSystem(mode='pre-validation', handler=MyHandler())
results = form.process_form(form_data)
```

## Navigation

### Menu Navigation

| Key | Action |
|-----|--------|
| **↑/↓** | Navigate menu |
| **1-9** | Jump to item |
| **Enter** | Select item |
| **ESC** | Back/Exit |
| **Space** | Toggle (multi-select) |
| **Ctrl+C** | Force exit |

### Form Navigation

- **Text input:** Type normally, Enter to submit
- **Choice field:** ↑/↓ or ←/→ to select, Enter to confirm
- **Multi-choice:** ↑/↓ to navigate, Space to toggle, Enter to confirm

## API Reference

### `@MenuItemCmd(cmd, params=[], options=[])`

Decorator for menu actions:

```python
@MenuItemCmd(
    "hello",
    params=[
        {'name': 'name', 'type': 'text', 'description': 'Your name'}
    ],
    options=[
        {'name': 'greeting', 'type': 'choice', 'choices': ['Hi', 'Hello', 'Hey']}
    ]
)
def hello(self, params, options):
    name = params.get('name', '')
    greeting = options.get('greeting', 'Hello')
    print(f"{greeting}, {name}!")
    return True
```

**Parameters:**
- `cmd` (str): Unique command identifier
- `params` (list): Required parameters definition list
- `options` (list): Optional parameters definition list

**Returns:** `True` to keep menu open, `False` to exit

### `ConsoleApp.__init__(name)`

Initialize application with menu system:

```python
app = ConsoleApp("My Application")
```

### `ConsoleApp.run()`

Display menu and start interactive loop:

```python
app.run()
```

### `Menu.register(*functions, config_path)`

Register decorated methods and load menu configuration:

```python
menu = Menu(title="Main Menu")
menu.register(
    app.method1,
    app.method2,
    config_path="menu_config.json"
)
```

### `FormSystem(mode, handler=None, endpoint=None)`

Create form processor:

```python
form = FormSystem(mode='interactive', handler=MyHandler())
results = form.process_form(form_data)
```

**Modes:**
- `interactive` - Process with callbacks
- `submit` - Auto-submit to endpoint
- `pre-validation` - Suggest values with callbacks

## Complete Example

**menu_config.json:**
```json
{
  "menu": [
    {"cmd": "greeting", "label": "Say Hello", "icon": "👋"},
    {
      "label": "Tools",
      "items": [
        {"cmd": "calc", "label": "Calculator", "icon": "🧮"}
      ]
    }
  ]
}
```

**console_app.py:**
```python
from menu_system import MenuItemCmd

class ConsoleApp:
    @MenuItemCmd("greeting")
    def hello_world(self, params, options):
        print("\n👋 Hello!")
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
    def show_calculator(self, params, options):
        num1 = float(params.get('num1', 0))
        num2 = float(params.get('num2', 0))
        operation = options.get('operation', 'add')
        
        if operation == 'add':
            result = num1 + num2
        else:
            result = 0
        
        print(f"\n{num1} + {num2} = {result}")
        return True
```

**main.py:**
```python
from console_app import ConsoleApp

if __name__ == "__main__":
    app = ConsoleApp("Demo App")
    app.run()
```

## Best Practices

1. **Menu Structure** - Keep JSON organized and readable
2. **Parameters** - Use type validation (number, choice) for params
3. **Options** - Use CLI-style format (`--key value`)
4. **Error Handling** - Gracefully handle user input errors
5. **Return Values** - Return `True` to stay, `False` to exit
6. **Icons** - Use consistent Unicode symbols
7. **Descriptions** - Provide clear help text for all items
8. **Validation** - Use `validation_rule` for params (required, min_length, range, etc.)

## Keyboard Shortcuts

| Shortcut | Function |
|----------|----------|
| Arrow keys | Navigate |
| Number keys | Jump to item |
| Enter | Select |
| ESC | Go back |
| Space | Toggle selection |
| Ctrl+C | Emergency exit |

---

**Built with Python • Cross-platform • Interactive • Extensible**

For more information, check the source code in `menu_system.py` and `form_system.py`.
