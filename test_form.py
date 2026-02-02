#!/usr/bin/env python3
"""Quick test of form interactive mode with new unified handler pattern."""

from console_app import ConsoleApp, FormFieldHandler
from form_system import FormSystem
import os

# Test the interactive form with after_input callbacks
app = ConsoleApp('ZMENU DEMO APP')

# Create handler with new after_input_* pattern
handler = FormFieldHandler()

# Initialize FormSystem in interactive mode
form_system = FormSystem(mode='interactive', handler=handler)

# Load form from JSON file
form_file = os.path.join(os.path.dirname(__file__), 'form_example.json')

print("Testing FormSystem with unified handler pattern:")
print("- before_input_* methods (called before user input)")
print("- after_input_* methods (called after user input)")
print()

if os.path.exists(form_file):
    form_data = form_system.load_form_from_file(form_file)
    form_definition = form_data.get('form', {})
    
    results = form_system.process_form(form_definition)
    
    if results:
        form_system.print_results(results)
else:
    print(f"Form file not found: {form_file}")
