# Multi-Level Menu Console Application

A flexible Python console application framework that supports nested menus at multiple levels.

## Features

✨ **Key Features:**
- Multi-level nested menu support
- Clean, user-friendly console interface
- Easy to extend with new options
- Error handling and input validation
- Automatic "Back" navigation between menu levels
- Exit functionality at any menu level

## Project Structure

```
console_app/
├── menu_system.py      # Core menu system framework
├── main.py             # Example application with multi-level menus
└── README.md           # This file
```

## Installation & Running

### Prerequisites
- Python 3.6 or higher

### Running the Application

```bash
python main.py
```

## How to Use

1. **Navigate menus** using numbers (1, 2, 3, etc.)
2. **Go back** to parent menu using the "Back" option
3. **Exit** by pressing `0` at any menu level
4. **Follow prompts** for actions that require input

### Example Menu Navigation

```
My Console Application
├── Say Hello
├── Greet User
├── Tools
│   ├── Calculator
│   └── System Information
├── Settings
│   ├── Display Options
│   │   ├── Change Theme
│   │   └── Change Font Size
│   └── Language
│       ├── English
│       ├── Español
│       └── Français
└── Help
    ├── About
    ├── How to Use
    └── Keyboard Shortcuts
```

## Customization Guide

### Adding a Simple Menu Item

```python
main_menu.add_item("key", "Display Label", action_function)
```

**Example:**
```python
def my_action():
    print("Hello World!")
    return True

main_menu.add_item("hello", "👋 Say Hello", my_action)
```

### Adding a Submenu

```python
submenu = main_menu.add_submenu("key", "Submenu Label")
submenu.add_item("item1", "Item 1", action_function)
submenu.add_item("item2", "Item 2", action_function)
```

**Example:**
```python
tools = main_menu.add_submenu("tools", "🛠️ Tools")
tools.add_item("calc", "Calculator", show_calculator)
tools.add_item("info", "System Info", show_system_info)
```

### Creating Multi-Level Submenus

```python
# Add submenu to main menu
settings = main_menu.add_submenu("settings", "⚙️ Settings")

# Add submenu to submenu
display = settings.add_submenu("display", "Display")

# Add items to nested submenu
display.add_item("theme", "Change Theme", set_theme)
```

### Action Function Requirements

- Must be callable (function or lambda)
- Should return `True` to continue the menu, `False` to exit
- Can accept input and display output
- Should handle exceptions gracefully

**Example:**
```python
def validate_age():
    try:
        age = int(input("Enter your age: "))
        if 0 <= age <= 150:
            print(f"You are {age} years old")
            return True
        else:
            print("Invalid age")
            return True  # Stay in menu
    except ValueError:
        print("Please enter a valid number")
        return True  # Stay in menu
```

## Built-in Examples

The included `main.py` demonstrates:

1. **Basic Menu Items**
   - Simple actions like "Say Hello"
   - Actions with user input like "Greet User"

2. **Tools Submenu**
   - Calculator (demonstrates computation)
   - System Information (demonstrates data display)

3. **Settings Submenu (Multi-level)**
   - Display Options (theme, font)
   - Language Selection

4. **Help Submenu**
   - About information
   - Usage instructions
   - Keyboard shortcuts

## Advanced Usage

### Creating a Custom Application

```python
from menu_system import ConsoleApp

# Create app
app = ConsoleApp("My App")
menu = app.get_menu()

# Add items and submenus
menu.add_item("opt1", "Option 1", my_function)
submenu = menu.add_submenu("sub", "Submenu")
submenu.add_item("opt2", "Option 2", another_function)

# Run
app.run()
```

### Handling Complex Data

```python
def process_data():
    user_input = input("Enter data: ")
    # Process the input
    result = analyze(user_input)
    print(f"Result: {result}")
    return True  # Continue menu

menu.add_item("process", "Process Data", process_data)
```

## Architecture

### Core Classes

- **MenuItem**: Represents a single menu option with an action
- **Menu**: Manages menu items, submenus, display, and user input
- **ConsoleApp**: Main application wrapper

### Menu Flow

```
User selects option
    ↓
Menu validates input
    ↓
Execute action or open submenu
    ↓
Display menu again (or close if exit)
```

## Tips & Best Practices

1. **Use Emojis** for better visual appeal
   ```python
   menu.add_item("calc", "🧮 Calculator", show_calculator)
   ```

2. **Keep Action Functions Simple** - Complex logic should be in separate modules

3. **Always Return Boolean** from action functions to indicate continuation

4. **Handle Exceptions** in action functions gracefully

5. **Test Navigation** - Verify back/exit options work at all levels

6. **Organize Logically** - Group related options in submenus

## Troubleshooting

**Q: Menu doesn't display properly on my terminal**
- A: Adjust terminal size or modify `_display_header()` width

**Q: Back option appears at top level**
- A: Normal behavior - back option only shows in submenus

**Q: Action doesn't execute**
- A: Verify action function returns True/False and doesn't raise exceptions

## License

This is a demonstration project. Feel free to use and modify as needed.

## Contributing

To enhance this application:
1. Add new menu items following the existing patterns
2. Create action functions with clear purposes
3. Test navigation at all menu levels
4. Update documentation for new features
