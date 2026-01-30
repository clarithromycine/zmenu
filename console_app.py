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
        """Setup and register all menu items."""
        main_menu = self.main_menu
        
        decorated_methods = []
        members = inspect.getmembers(self, predicate=inspect.ismethod)
        for name, method in members:
            if hasattr(method, 'cmd'):  
                decorated_methods.append(method)
        
        # Pass MENU_GROUP to register method for validation
        main_menu.register(*decorated_methods, allowed_groups=self.MENU_GROUP)
        
        # Update group icons and names, and collect group info
        for group_path, group_config in self.MENU_GROUP.items():
            icon = group_config.get("icon", "")
            display_name = group_config.get("name", "")
            
            path_parts = group_path.split('.')
            current_menu = main_menu
            
            for i in range(len(path_parts) - 1):
                submenu_key = '.'.join(path_parts[:i+1])
                if submenu_key in current_menu.submenus:
                    current_menu = current_menu.submenus[submenu_key]
            
            final_key = path_parts[-1] if len(path_parts) == 1 else '.'.join(path_parts)
            
            if final_key in current_menu.items:
                current_menu.items[final_key].label = f"{icon} {display_name} >"
        
        # Re-sort root menu items based on order from MENU_GROUP and MenuItemCmd
        self._resort_menu(main_menu)

    def _resort_menu(self, menu: Menu) -> None:
        """Re-sort menu items based on MENU_GROUP and MenuItemCmd orders.
        
        Sorting priority:
        1. Items without group and items with group are mixed and sorted by their order
        2. Items without group use MenuItemCmd order
        3. Groups use MENU_GROUP order
        """
        # Build order map for all items
        item_order_map = {}
        
        # Collect order from decorated methods
        members = inspect.getmembers(self, predicate=inspect.ismethod)
        for name, method in members:
            if hasattr(method, 'cmd'):
                cmd = getattr(method, 'cmd', None)
                order = getattr(method, 'order', 0)
                group = getattr(method, 'group', None)
                if group is None:
                    # Root menu items: (order_value, item_key)
                    item_order_map[cmd] = (order, cmd)
        
        # Collect group orders from MENU_GROUP
        for group_key, group_config in self.MENU_GROUP.items():
            # Only consider first-level groups (no dot in name)
            if '.' not in group_key:
                group_order = group_config.get('order', 999)
                item_order_map[group_key] = (group_order, group_key)
        
        # Sort menu._item_order based on the order value
        def get_sort_key(key):
            if key in item_order_map:
                order_val, item_key = item_order_map[key]
                return (order_val, item_key)
            else:
                # Items not in map go to the end
                return (999, key)
        
        menu._item_order.sort(key=get_sort_key)
    
    def run(self) -> None:
        self.main_menu.display()

    # Group configuration for visual customization and ordering
    # Only groups defined here will be displayed
    MENU_GROUP = {
        "Tools":                  {"icon": "🛠️", "name": "Tools", "order": 1},
        "nLevel":                 {"icon": "📁", "name": "N-Level Menu Demo", "order": 2},
        "nLevel.Display":         {"icon": "📺", "name": "Display Options", "order": 1},
        "nLevel.Language":        {"icon": "🌐", "name": "Language", "order": 2}
    }

    # Menu item action methods
    @MenuItemCmd("greeting", "Say Hello", order=0, icon="👋", long_desc="Display a friendly greeting message")
    def hello_world(self):
        """Simple hello world action."""
        print("\n👋 Hello from the console app!")
        return True

    @MenuItemCmd("calc", "Calculator", order=0, group="Tools", icon="🧮", long_desc="Perform basic arithmetic operations")
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

    @MenuItemCmd("sysinfo", "System Information", order=1, group="Tools", icon="ℹ️", long_desc="Display system and environment details")
    def show_system_info(self):
        """Display system information."""
        print(f"\nOperating System: {sys.platform}")
        print(f"Python Version: {sys.version.split()[0]}")
        print(f"Current Directory: {os.getcwd()}")
        return True

    @MenuItemCmd("theme", "Change Theme", group="nLevel.Display", icon="🎨", long_desc="Customize the visual appearance")
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

    @MenuItemCmd("font", "Change Font Size", group="nLevel.Display", icon="🔠", long_desc="Adjust text size for better readability")
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

    @MenuItemCmd("en", "English", group="nLevel.Language", long_desc="Set interface language to English")
    def set_language_en(self):
        """Set language to English."""
        print(f"\n✅ Language changed to: English")
        return True

    @MenuItemCmd("es", "Español", group="nLevel.Language", long_desc="Cambiar idioma de interfaz al español")
    def set_language_es(self):
        """Set language to Español."""
        print(f"\n✅ Language changed to: Español")
        return True

    @MenuItemCmd("fr", "Français", group="nLevel.Language", long_desc="Définir la langue de l'interface au français")
    def set_language_fr(self):
        """Set language to Français."""
        print(f"\n✅ Language changed to: Français")
        return True


    @MenuItemCmd("time", "Show Time", order=2, group="Tools", icon="🕐", long_desc="Display the current date and time")
    def show_time(self):
        """Display current time."""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n  Current time: {current_time}")
        return True

    @MenuItemCmd("confirm", "Confirm Demo", order=3, icon="✅", long_desc="Test the yes/no selection with arrow keys")
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

    @MenuItemCmd("multi", "Multi-Select Demo", order=5, icon="☑️", long_desc="Test multi-select with checkboxes")
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

    @MenuItemCmd("form", "Form Demo", order=6, icon="📋", long_desc="Fill out an interactive form with multiple field types")
    def form_demo(self):
        """Demonstrate the interactive form system."""
        form_system = FormSystem()
        
        # Load form from JSON file
        form_file = os.path.join(os.path.dirname(__file__), 'form_example.json')
        
        if not os.path.exists(form_file):
            print(f"\n❌ 表单文件未找到: {form_file}")
            return True
        
        try:
            form_data = form_system.load_form_from_file(form_file)
            form_definition = form_data.get('form', {})
            
            # Process the form
            results = form_system.process_form(form_definition)
            
            # Check if form was cancelled (results is None)
            if results is None:
                return True
            
            # Display results
            form_system.print_results(results)
            
            # Save results
            result_file = os.path.join(os.path.dirname(__file__), 'form_result.json')
            form_system.save_results(results, result_file)
            
        except json.JSONDecodeError:
            print(f"\n❌ 表单文件格式错误")
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")
        
        return True

    @MenuItemCmd("form_interactive", "Form Interactive Mode", order=7, icon="📝", long_desc="Form with immediate field processing (interactive mode)")
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

    @MenuItemCmd("form_submit", "Form Submit Mode", order=8, icon="📤", long_desc="Form with automatic submission (submit mode)")
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
