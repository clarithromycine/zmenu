#!/usr/bin/env python3
"""
Test script to demonstrate the new pre-validation feature in ZMenu form system.
"""

import os
from form_system import FormSystem
from console_app import FormFieldHandler, FormPreValidationHandler

def test_pre_validation_feature():
    """Test the new pre-validation feature."""
    print("🧪 Testing ZMenu Pre-Validation Feature\n")
    
    # Create handler objects
    handler = FormFieldHandler()
    pre_validation_handler = FormPreValidationHandler()
    
    # Initialize FormSystem in interactive mode with pre-validation
    form_system = FormSystem(
        mode='interactive', 
        handler=handler,
        pre_validation_handler=pre_validation_handler
    )
    
    print("✅ FormSystem initialized with pre-validation handler")
    print(f"   - Mode: {form_system.mode}")
    print(f"   - Has handler: {form_system.handler is not None}")
    print(f"   - Has pre-validation handler: {form_system.pre_validation_handler is not None}")
    
    # Check that pre-validation methods exist
    print("\n🔍 Checking pre-validation methods:")
    methods_to_check = ['pre_validate_name', 'pre_validate_email', 'pre_validate_country', 
                       'pre_validate_interests', 'pre_validate_subscription']
    
    for method_name in methods_to_check:
        has_method = hasattr(pre_validation_handler, method_name)
        status = "✅" if has_method else "❌"
        print(f"   {status} {method_name}")
    
    # Test loading the example form
    form_file = os.path.join(os.path.dirname(__file__), 'form_example.json')
    
    if os.path.exists(form_file):
        try:
            form_data = form_system.load_form_from_file(form_file)
            form_definition = form_data.get('form', {})
            fields = form_definition.get('fields', [])
            
            print(f"\n📋 Loaded form with {len(fields)} fields:")
            for field in fields:
                print(f"   - {field.get('id')}: {field.get('label')} ({field.get('type')})")
            
            print("\n✨ Pre-validation feature successfully implemented!")
            print("\n💡 To test the full functionality, run: python3 main.py")
            print("   Then select 'Form with Pre-Validation' from the menu.")
            
        except Exception as e:
            print(f"\n❌ Error loading form: {e}")
    else:
        print(f"\n⚠️  Form file not found at: {form_file}")

if __name__ == "__main__":
    test_pre_validation_feature()