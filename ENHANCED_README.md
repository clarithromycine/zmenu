# ZMenu - Enhanced Form Pre-Validation Feature

## Overview

ZMenu has been enhanced with a new pre-validation feature that allows checking for existing values before prompting users for input in forms. This feature enables the system to suggest default values or skip certain fields based on previously stored data.

## New Pre-Validation Feature

### FormSystem Constructor Changes

The `FormSystem` constructor now accepts an additional `pre_validation_handler` parameter:

```python
form_system = FormSystem(
    mode='interactive',           # 'interactive' or 'submit'
    handler=field_handler,        # Handler for post-input callbacks
    pre_validation_handler=pre_validation_handler,  # Handler for pre-validation (optional)
    endpoint=None                 # API endpoint for submit mode
)
```

### Pre-Validation Handler Implementation

To use the pre-validation feature, create a handler class with methods named `pre_validate_{field_id}`:

```python
class FormPreValidationHandler:
    def __init__(self):
        # Sample existing data for demonstration
        self.existing_data = {
            "name": "Kenny Zhang",
            "email": "kenny@example.com",
            "country": "cn",
            "interests": ["tech", "music"],
            "subscription": "pro"
        }
    
    def pre_validate_name(self, field, current_results):
        """Pre-validate name field."""
        if "name" in self.existing_data:
            return self.existing_data["name"]
        return None
    
    def pre_validate_email(self, field, current_results):
        """Pre-validate email field."""
        if "email" in self.existing_data:
            return self.existing_data["email"]
        return None
    
    # Additional pre-validation methods for other fields...
```

### How Pre-Validation Works

1. **Before prompting for input**, the system checks if a pre-validation handler exists
2. **Calls the appropriate pre-validation method** based on the field ID
3. **If a pre-validated value is returned**, the system displays it as a suggestion
4. **Asks the user for confirmation** whether to use the existing value or proceed with input
5. **If confirmed**, uses the pre-validated value and skips the input prompt

### Pre-Validation Method Signature

Each pre-validation method should follow this signature:

```python
def pre_validate_{field_id}(self, field, current_results):
    """
    Pre-validate a field before user input.
    
    Args:
        field: The FormField object containing field metadata
        current_results: Dictionary of results collected so far in the form
        
    Returns:
        Pre-validated value if available, None otherwise
    """
    # Implementation here
    pass
```

### Supported Field Types

The pre-validation feature works with all field types:

- **Text fields**: Suggests the existing text value
- **Single choice fields**: Pre-selects the matching option
- **Multi-choice fields**: Pre-selects the matching options (expects a list of values)

### Benefits

1. **Improved User Experience**: Reduces repetitive data entry by suggesting existing values
2. **Faster Form Completion**: Users can quickly accept defaults instead of re-entering known information
3. **Data Consistency**: Helps maintain consistency by reusing validated values
4. **Flexible Implementation**: Can be used selectively for specific fields or forms

### Example Usage

```python
# Create a pre-validation handler with existing data
pre_validator = FormPreValidationHandler()

# Initialize form system with pre-validation
form_system = FormSystem(
    mode='interactive',
    handler=FormFieldHandler(),  # Post-input callbacks
    pre_validation_handler=pre_validator  # Pre-validation callbacks
)

# Load and process form
form_data = form_system.load_form_from_file('form_example.json')
results = form_system.process_form(form_data['form'])
```

## Integration with Existing Features

The pre-validation feature seamlessly integrates with:

- **Interactive mode**: Shows existing values and confirms with user before proceeding
- **Submit mode**: Could be extended to pre-populate forms with existing data
- **All field types**: Text, single choice, and multi-choice fields
- **Cross-platform support**: Works on Windows, macOS, and Linux
- **Form validation**: Respects existing validation rules even with pre-validated values

## API Changes Summary

- Added `pre_validation_handler` parameter to `FormSystem.__init__()`
- Added `_check_pre_validation()` method to perform pre-validation checks
- Added `_confirm_use_existing_value()` method for user confirmation
- Updated all input methods (`_get_text_input`, `_get_single_choice`, `_get_multi_choice`) to support pre-validation