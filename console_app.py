"""
Console Application with Menu System
Main application class for managing menus and application flow.
"""
import sys, os, inspect, datetime, json
from menu_system import Menu, MenuItemCmd
from form_system import FormSystem
    
class ConsoleApp:
    """Main console application with menu system."""
            
    def __init__(self, name: str = "Console App"):
        self.name = name
        self.main_menu = Menu(title=name)
        self.setup_menu()

    def setup_menu(self) -> None:
        """Setup and register all menu items.
        
        Menu configuration is loaded from menu_config.json in hierarchical structure.
        This method collects decorated methods and passes them to register().
        """
        main_menu = self.main_menu
        
        decorated_methods = []
        members = inspect.getmembers(self, predicate=inspect.ismethod)
        for name, method in members:
            if hasattr(method, 'cmd'):  
                decorated_methods.append(method)
        
        # Load menu configuration from JSON file in this directory
        config_path = os.path.join(os.path.dirname(__file__), 'menu_config.json')
        
        # register() will load hierarchical menu structure from JSON and follow that order
        main_menu.register(*decorated_methods, config_path=config_path)

    def run(self) -> None:
        self.main_menu.display()

    # Menu item action methods
    @MenuItemCmd("greeting")
    def hello_world(self, params, options):
        """Simple hello world action."""
        print("\n👋 Hello from the console app!")
        return True

    @MenuItemCmd(
        "calc",
        params=[
            {'name': 'num1', 'type': 'number', 'description': 'First number', 'validation_rule': 'required'},
            {'name': 'num2', 'type': 'number', 'description': 'Second number', 'validation_rule': 'required'},
        ],
        options=[
            {'name': 'operation', 'type': 'choice', 'description': 'Operation','choices': ['add', 'subtract', 'multiply', 'divide']},
            {'name': 'text', 'type': 'string', 'description': 'a string text'},
        ]
    )
    def show_calculator(self, params, options):
        """Calculator with parameter collection.
        
        Args:
            params: Dict with 'num1' and 'num2'
            options: Dict with 'operation'
        """

        try:
            num1 = float(params.get('num1', 0))
            num2 = float(params.get('num2', 0))
            operation = options.get('operation', 'add')

            print(options.get('text', 'no value'))
            
            result = None            
            if operation == 'add':
                result = num1 + num2
                op_symbol = '+'
            elif operation == 'subtract':
                result = num1 - num2
                op_symbol = '-'
            elif operation == 'multiply':
                result = num1 * num2
                op_symbol = '×'
            elif operation == 'divide':
                if num2 == 0:
                    print("\n❌ Division by zero not allowed")
                    return True
                result = num1 / num2
                op_symbol = '÷'
            else:                
                print(f"\n❌ Unknown operation: {operation}")
                return True
            
            print(f"\n  {num1} {op_symbol} {num2} = {result}")
        except ValueError:
            print("\n❌ Invalid number input")
        except KeyboardInterrupt:
            print("\n\n⏹️  Operation cancelled by user")
        
        return True

    @MenuItemCmd("sysinfo")
    def show_system_info(self, params, options):
        """Display system information."""
        print(f"\nOperating System: {sys.platform}")
        print(f"Python Version: {sys.version.split()[0]}")
        print(f"Current Directory: {os.getcwd()}")
        return True

    @MenuItemCmd("theme")
    def show_theme_options(self, params, options):
        """Display theme options."""
        print("\n" + "=" * 60)
        print("  THEME OPTIONS")
        print("=" * 60)
        print("\n  Available themes:")
        print("    • Light")
        print("    • Dark")
        print("    • High Contrast")
        print("\n  [This is a demonstration - feature not fully implemented]")
        return True

    @MenuItemCmd("font")
    def show_font_options(self, params, options):
        """Display font size options."""
        print("\n" + "=" * 60)
        print("  FONT SIZE OPTIONS")
        print("=" * 60)
        print("\n  Available sizes:")
        print("    • Small (8pt)")
        print("    • Medium (12pt)")
        print("    • Large (16pt)")
        print("\n  [This is a demonstration - feature not fully implemented]")
        return True

    @MenuItemCmd("en")
    def set_language_en(self, params, options):
        """Set language to English."""
        print(f"\n✅ Language changed to: English")
        return True

    @MenuItemCmd("es")
    def set_language_es(self, params, options):
        """Set language to Español."""
        print(f"\n✅ Language changed to: Español")
        return True

    @MenuItemCmd("fr")
    def set_language_fr(self, params, options):
        """Set language to Français."""
        print(f"\n✅ Language changed to: Français")
        return True


    @MenuItemCmd("time")
    def show_time(self, params, options):
        """Display current time."""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n  Current time: {current_time}")
        return True

    @MenuItemCmd("confirm")
    def confirm_demo(self, params, options):
        """Demonstrate the yes/no prompt with left/right arrow keys."""
        result = self.main_menu.yes_no_prompt(
            question="Do you want to continue?",
            description="Use LEFT/RIGHT arrow keys to select, then press ENTER"
        )
        
        if result is True:
            print("\n✓ You selected: YES")
        elif result is False:
            print("\n✗ You selected: NO")
        else:
            print("\n⊘ You cancelled the operation")
        
        return True

    @MenuItemCmd("multi")
    def multi_select_demo(self, params, options):
        """Demonstrate the multi-select prompt."""
        try:
            items = [            
                {"label": "🌐 Enable Dark Mode", "description": "Use dark theme across the application", "selected": False},
                {"label": "🔔 Enable Notifications", "description": "Show system notifications", "selected": True},
                {"label": "📊 Analytics", "description": "Send usage analytics", "selected": False},
                {"label": "🔒 Enable Two-Factor Auth", "description": "Require 2FA for login", "selected": True},
                {"label": "🌍 Auto-Update", "description": "Automatically check for updates", "selected": False},
                {"label": "💾 Auto-Save", "description": "Automatically save your work", "selected": True},
                {"label": "🔊 Sound Effects", "description": "Enable UI sound effects", "selected": False},
            ]
            
            selected = self.main_menu.multi_select_prompt("Select packages to install", items)
            
            if selected is None:
                print("\n⊘ Selection cancelled")
            else:
                print("\n✓ Selected items:")
                for item in selected:
                    print(f"  • {item['label']}")
        except KeyboardInterrupt:
            print("\n\n⏹️  Operation cancelled by user")
        
        return True

    @MenuItemCmd("form_interactive")
    def form_interactive_demo(self, params, options):
        """Demonstrate the form system in interactive mode with field callbacks."""
        # Create a handler object with callback methods
        handler = FormFieldHandler()
        
        # Initialize FormSystem in interactive mode
        form_system = FormSystem(mode='interactive', handler=handler)
        
        # Load form from JSON file
        form_file = os.path.join(os.path.dirname(__file__), 'form_example.json')
        
        if not os.path.exists(form_file):
            print(f"\n❌ 表单文件未找到: {form_file}")
            return True
        
        try:
            form_data = form_system.load_form_from_file(form_file)
            form_definition = form_data.get('form', {})
            
            # Process the form - callbacks will be triggered for each field
            results = form_system.process_form(form_definition)
            
            if results is None:
                return True
            
            # Display results
            form_system.print_results(results)
            
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")
        
        return True

    @MenuItemCmd("form_submit")
    def form_submit_demo(self, params, options):
        """Demonstrate the form system in submit mode."""
        # Initialize FormSystem in submit mode
        # Set endpoint to None for local processing, or provide API endpoint for actual submission
        form_system = FormSystem(mode='submit', endpoint=None)
        
        # Load form from JSON file
        form_file = os.path.join(os.path.dirname(__file__), 'form_example.json')
        
        if not os.path.exists(form_file):
            print(f"\n❌ 表单文件未找到: {form_file}")
            return True
        
        try:
            form_data = form_system.load_form_from_file(form_file)
            form_definition = form_data.get('form', {})
            
            # Process the form - results will be automatically submitted at the end
            results = form_system.process_form(form_definition)
            
            if results is None:
                return True
            
            # Display results
            form_system.print_results(results)
            
            # Save results
            result_file = os.path.join(os.path.dirname(__file__), 'form_submit_result.json')
            form_system.save_results(results, result_file)
            
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")
        
        return True

    @MenuItemCmd("form_validation")
    def form_pre_validation_demo(self, params, options):
        """Demonstrate the form system with pre-validation functionality."""
        # Create a combined handler with both before_input_* and after_input_* methods
        handler = CombinedFormHandler()
        
        # Initialize FormSystem in interactive mode
        # The handler now includes both before_input_* and after_input_* methods
        form_system = FormSystem(
            mode='interactive', 
            handler=handler
        )
        
        # Load form from JSON file
        form_file = os.path.join(os.path.dirname(__file__), 'form_example.json')
        
        if not os.path.exists(form_file):
            print(f"\n❌ 表单文件未找到: {form_file}")
            return True
        
        try:
            form_data = form_system.load_form_from_file(form_file)
            form_definition = form_data.get('form', {})
            
            # Process the form with pre-validation and post-processing
            results = form_system.process_form(form_definition)
            
            if results is None:
                return True
            
            # Display results
            form_system.print_results(results)
            
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")
        
        return True


class FormFieldHandler:
    """Handler for form field callbacks using unified pattern.
    
    Pattern:
    - before_input_<field_id>(field, current_results) -> Optional[value]
      Called before prompting user; can suggest pre-validated values
    - after_input_<field_id>(value, field, current_results) -> None
      Called after user input collected; for immediate processing
    """
    
    def after_input_name(self, value, field, results):
        """Called after 'name' field is completed."""
        if value:
            print(f"  📌 Processing: Name validation...")
            if len(value) < 2:
                print(f"  ⚠️  Warning: Name is very short")
            else:
                print(f"  ✓ Name '{value}' is valid")
        else:
            print(f"  ⚠️  Name field skipped")
    
    def after_input_email(self, value, field, results):
        """Called after 'email' field is completed."""
        if value:
            print(f"  📌 Processing: Email validation...")
            if '@' in value:
                print(f"  ✓ Email format looks good: {value}")
            else:
                print(f"  ⚠️  Warning: Email might be invalid")
        else:
            print(f"  ⚠️  Email field skipped")
    
    def after_input_country(self, value, field, results):
        """Called after 'country' field is completed."""
        if value:
            print(f"  📌 Processing: Country selection...")
            print(f"  ✓ Selected region: {value}")
        else:
            print(f"  ⚠️  Country field skipped")
    
    def after_input_interests(self, value, field, results):
        """Called after 'interests' field is completed."""
        print(f"  📌 Processing: Interest selections...")
        if isinstance(value, list) and value:
            print(f"  ✓ Selected {len(value)} interests")
        else:
            print(f"  ⚠️  No interests selected")
    
    def after_input_plan(self, value, field, results):
        """Called after 'plan' field is completed."""
        if value:
            print(f"  📌 Processing: Subscription plan...")
            print(f"  ✓ Plan selected: {value}")
        else:
            print(f"  ⚠️  Plan field skipped")
    
    def after_input_bio(self, value, field, results):
        """Called after 'bio' field is completed."""
        if value:
            print(f"  📌 Processing: Bio content...")
            print(f"  ✓ Bio length: {len(value)} characters")
        else:
            print(f"  ⚠️  Bio field skipped")


class FormPreValidationHandler:
    """Handler for form before_input callbacks.
    
    Pattern:
    - before_input_<field_id>(field, current_results) -> Optional[value]
      Called before prompting user; can suggest pre-validated values
    """
    
    def __init__(self):
        # Sample existing data for demonstration
        self.existing_data = {
            "name": "Kenny Zhang",
            "email": "kenny@example.com",
            "country": "cn",
            "interests": ["tech", "music"],
            "subscription": "pro"
        }
    
    def before_input_name(self, field, current_results):
        """Suggest value before 'name' field input."""        
        if "name" in self.existing_data:
            return self.existing_data["name"]
        return None
    
    def before_input_email(self, field, current_results):
        """Suggest value before 'email' field input."""
        if "email" in self.existing_data:
            return self.existing_data["email"]
        return None
    
    def before_input_country(self, field, current_results):
        """Suggest value before 'country' field input."""
        if "country" in self.existing_data:
            return self.existing_data["country"]
        return None
    
    def before_input_interests(self, field, current_results):
        """Suggest value before 'interests' field input."""
        if "interests" in self.existing_data:
            return self.existing_data["interests"]
        return None
    
    def before_input_subscription(self, field, current_results):
        """Suggest value before 'subscription' field input."""
        if "subscription" in self.existing_data:
            return self.existing_data["subscription"]
        return None
    
    def before_input_bio(self, field, current_results):
        """Suggest value before 'bio' field input."""
        # Don't provide a default for bio since it's usually unique
        return None


class CombinedFormHandler(FormFieldHandler, FormPreValidationHandler):
    """Combined handler with both before_input_* and after_input_* methods.
    
    Inherits:
    - before_input_* methods from FormPreValidationHandler (suggest values)
    - after_input_* methods from FormFieldHandler (process values)
    
    This is the recommended pattern for forms that need both pre-validation
    and post-processing functionality.
    """
    pass

