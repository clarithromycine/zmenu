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
    def hello_world(self):
        """Simple hello world action."""
        print("\n👋 Hello from the console app!")
        return True

    @MenuItemCmd("calc")
    def show_calculator(self):
        """Simple calculator demonstration."""
        try:
            num1 = float(input("\nEnter first number: "))
            num2 = float(input("Enter second number: "))
            
            print(f"\n  {num1} + {num2} = {num1 + num2}")
            print(f"  {num1} - {num2} = {num1 - num2}")
            print(f"  {num1} × {num2} = {num1 * num2}")
            if num2 != 0:
                print(f"  {num1} ÷ {num2} = {num1 / num2}")
            else:
                print(f"  Division by zero not allowed")
        except ValueError:
            print("\n❌ Invalid number input")
        except KeyboardInterrupt:
            print("\n\n⏹️  Operation cancelled by user")
        
        return True

    @MenuItemCmd("sysinfo")
    def show_system_info(self):
        """Display system information."""
        print(f"\nOperating System: {sys.platform}")
        print(f"Python Version: {sys.version.split()[0]}")
        print(f"Current Directory: {os.getcwd()}")
        return True

    @MenuItemCmd("theme")
    def show_theme_options(self):
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
    def show_font_options(self):
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
    def set_language_en(self):
        """Set language to English."""
        print(f"\n✅ Language changed to: English")
        return True

    @MenuItemCmd("es")
    def set_language_es(self):
        """Set language to Español."""
        print(f"\n✅ Language changed to: Español")
        return True

    @MenuItemCmd("fr")
    def set_language_fr(self):
        """Set language to Français."""
        print(f"\n✅ Language changed to: Français")
        return True


    @MenuItemCmd("time")
    def show_time(self):
        """Display current time."""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n  Current time: {current_time}")
        return True

    @MenuItemCmd("confirm")
    def confirm_demo(self):
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
    def multi_select_demo(self):
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
    def form_interactive_demo(self):
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
    def form_submit_demo(self):
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
    def form_pre_validation_demo(self):
        """Demonstrate the form system with pre-validation functionality."""
        # Create handler objects
        handler = FormFieldHandler()
        pre_validation_handler = FormPreValidationHandler()
        
        # Initialize FormSystem in interactive mode with pre-validation
        form_system = FormSystem(
            mode='interactive', 
            handler=handler,
            pre_validation_handler=pre_validation_handler
        )
        
        # Load form from JSON file
        form_file = os.path.join(os.path.dirname(__file__), 'form_example.json')
        
        if not os.path.exists(form_file):
            print(f"\n❌ 表单文件未找到: {form_file}")
            return True
        
        try:
            form_data = form_system.load_form_from_file(form_file)
            form_definition = form_data.get('form', {})
            
            # Process the form with pre-validation
            results = form_system.process_form(form_definition)
            
            if results is None:
                return True
            
            # Display results
            form_system.print_results(results)
            
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")
        
        return True


class FormFieldHandler:
    """Handler for form field callbacks in interactive mode."""
    
    def on_field_name(self, value, field):
        """Callback when 'name' field is completed."""
        if value:
            print(f"  📌 Processing: Name validation...")
            if len(value) < 2:
                print(f"  ⚠️  Warning: Name is very short")
            else:
                print(f"  ✓ Name '{value}' is valid")
        else:
            print(f"  ⚠️  Name field skipped")
    
    def on_field_email(self, value, field):
        """Callback when 'email' field is completed."""
        if value:
            print(f"  📌 Processing: Email validation...")
            if '@' in value:
                print(f"  ✓ Email format looks good: {value}")
            else:
                print(f"  ⚠️  Warning: Email might be invalid")
        else:
            print(f"  ⚠️  Email field skipped")
    
    def on_field_country(self, value, field):
        """Callback when 'country' field is completed."""
        if value:
            print(f"  📌 Processing: Country selection...")
            print(f"  ✓ Selected region: {value}")
        else:
            print(f"  ⚠️  Country field skipped")
    
    def on_field_interests(self, value, field):
        """Callback when 'interests' field is completed."""
        print(f"  📌 Processing: Interest selections...")
        if isinstance(value, list) and value:
            print(f"  ✓ Selected {len(value)} interests")
        else:
            print(f"  ⚠️  No interests selected")
    
    def on_field_plan(self, value, field):
        """Callback when 'plan' field is completed."""
        if value:
            print(f"  📌 Processing: Subscription plan...")
            print(f"  ✓ Plan selected: {value}")
        else:
            print(f"  ⚠️  Plan field skipped")
    
    def on_field_bio(self, value, field):
        """Callback when 'bio' field is completed."""
        if value:
            print(f"  📌 Processing: Bio content...")
            print(f"  ✓ Bio length: {len(value)} characters")
        else:
            print(f"  ⚠️  Bio field skipped")


class FormPreValidationHandler:
    """Handler for form pre-validation callbacks."""
    
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
    
    def pre_validate_country(self, field, current_results):
        """Pre-validate country field."""
        if "country" in self.existing_data:
            return self.existing_data["country"]
        return None
    
    def pre_validate_interests(self, field, current_results):
        """Pre-validate interests field."""
        if "interests" in self.existing_data:
            return self.existing_data["interests"]
        return None
    
    def pre_validate_subscription(self, field, current_results):
        """Pre-validate subscription field."""
        if "subscription" in self.existing_data:
            return self.existing_data["subscription"]
        return None
    
    def pre_validate_bio(self, field, current_results):
        """Pre-validate bio field."""
        # Don't provide a default for bio since it's usually unique
        return None
