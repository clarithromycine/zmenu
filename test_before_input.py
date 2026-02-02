#!/usr/bin/env python3
"""Quick test to verify before_input_* methods are being called."""

from console_app import CombinedFormHandler
from form_system import FormSystem
import os

# Patch the method to see if it's called
original_before_input_name = CombinedFormHandler.before_input_name

call_log = []

def logged_before_input_name(self, field, current_results):
    call_log.append(f"before_input_name called with field: {field.label}")
    return original_before_input_name(self, field, current_results)

CombinedFormHandler.before_input_name = logged_before_input_name

# Test the form
handler = CombinedFormHandler()
form_system = FormSystem(mode='interactive', handler=handler)

form_file = os.path.join(os.path.dirname(__file__), 'form_example.json')

if os.path.exists(form_file):
    print("Testing CombinedFormHandler with before_input_* methods\n")
    print("=" * 60)
    
    form_data = form_system.load_form_from_file(form_file)
    form_definition = form_data.get('form', {})
    
    # Just process first field to see if before_input_* is called
    results = form_system.process_form(form_definition)
    
    print("\n" + "=" * 60)
    print(f"\nCall log:")
    for call in call_log:
        print(f"  ✓ {call}")
    
    if call_log:
        print("\n✓ before_input_* methods ARE being called!")
    else:
        print("\n❌ before_input_* methods are NOT being called!")
else:
    print(f"Form file not found: {form_file}")
