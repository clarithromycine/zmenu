"""
MenuItemCmd Parameter System Documentation

The parameter system allows menu items to automatically collect user input
before executing the action function.

=== DEFINITION ===

@MenuItemCmd(
    cmd='command_id',
    params=[
        {
            'name': 'param_name',           # Unique parameter name
            'type': 'text|number|choice',   # Input type
            'description': 'Description',   # Shown to user
            'validation_rule': 'rule',      # Validation rule (see below)
            'choices': [...]                # For choice type only
        },
        ...
    ],
    options=[
        {
            'name': 'option_name',          # Unique option name
            'type': 'text|bool|choice',     # Input type
            'description': 'Description',   # Shown to user
            'default': 'value',             # Default value
            'choices': [...]                # For choice type only
        },
        ...
    ]
)
def my_command(params, options):
    # params: Dict with required parameters
    # options: Dict with optional parameters
    pass


=== VALIDATION RULES ===

Validation rules for parameters:
- 'required': Field must not be empty
- 'min_length:N': Minimum N characters
- 'max_length:N': Maximum N characters
- 'range:MIN-MAX': Numeric range (for number type)

Examples:
  {'name': 'age', 'type': 'number', 'validation_rule': 'range:1-150'}
  {'name': 'email', 'type': 'text', 'validation_rule': 'min_length:5'}
  {'name': 'username', 'type': 'text', 'validation_rule': 'required'}


=== TYPES ===

Parameter/Option Types:
- 'text': Free text input
- 'number': Numeric input (validates as number)
- 'choice': Select from predefined options
- 'bool' (options only): Yes/No toggle


=== PARAMETER vs OPTIONS ===

Parameters (params):
  - Required fields
  - User must provide a value
  - Shown first in the form
  - Uses validation_rule for validation

Options (options):
  - Optional fields
  - Can have default values
  - Shown after parameters
  - Use default value if user doesn't input


=== EXECUTION FLOW ===

1. User selects menu item
2. If item has params or options defined:
   a. Form is automatically generated
   b. User fills in the form
   c. Inputs are collected and validated
3. Function is called with (params, options) dictionaries
4. Function executes with the provided parameters


=== EXAMPLE ===

@MenuItemCmd(
    cmd='transfer',
    params=[
        {'name': 'amount', 'type': 'number', 'description': 'Transfer amount', 'validation_rule': 'range:1-10000'},
        {'name': 'recipient', 'type': 'text', 'description': 'Recipient account', 'validation_rule': 'required'},
    ],
    options=[
        {'name': 'priority', 'type': 'choice', 'description': 'Transfer priority', 'default': 'normal', 'choices': ['normal', 'express']},
        {'name': 'notify', 'type': 'bool', 'description': 'Send notification', 'default': True},
    ]
)
def transfer_funds(params, options):
    amount = params['amount']
    recipient = params['recipient']
    priority = options['priority']
    notify = options['notify']
    
    print(f"Transferring {amount} to {recipient} via {priority}")
    if notify:
        print("Notification enabled")
    
    return True


=== RETURN VALUES ===

The function should return:
- True: Continue showing the menu
- False: Exit and go back to parent menu
- Any other value: Treated as True
"""

# Quick Reference

PARAMETER_DEFINITION = {
    'name': str,                              # Required, unique identifier
    'type': 'text|number|choice',             # Required
    'description': str,                       # Optional, shown to user
    'validation_rule': 'required|min_length|max_length|range',  # Optional
    'choices': list,                          # Required for type='choice'
}

OPTION_DEFINITION = {
    'name': str,                              # Required, unique identifier
    'type': 'text|bool|choice',               # Required
    'description': str,                       # Optional, shown to user
    'default': str,                           # Optional, default value
    'choices': list,                          # Required for type='choice'
}
