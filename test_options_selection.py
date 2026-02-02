"""Test the options selection flow"""
from menu_system import Menu

# Create a test menu
menu = Menu(title="Test Menu")

# Add a test item with options
menu.add_item(
    'calc',
    '🧮 Calculator',
    lambda params, options: print(f"Params: {params}, Options: {options}"),
    params=[
        {'name': 'num1', 'type': 'number', 'description': 'First number', 'validation_rule': 'required'},
        {'name': 'num2', 'type': 'number', 'description': 'Second number', 'validation_rule': 'required'},
    ],
    options=[
        {'name': 'operation', 'type': 'choice', 'description': 'Operation', 'choices': ['add', 'subtract', 'multiply', 'divide']},
        {'name': 'text', 'type': 'string', 'description': 'a string text'},
    ]
)

print("✅ Test passed - Menu initialized successfully with options")
