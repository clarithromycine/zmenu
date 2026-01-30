"""
Interactive Form System for Console
Process form JSON and collect user input interactively.
"""
import json
from typing import Any, Dict, List, Optional
from menu_system import Menu


class FormField:
    """Represents a single form field."""
    
    def __init__(self, field_data: Dict[str, Any]):
        self.id = field_data.get('id', '')
        self.type = field_data.get('type', 'text')  # text, single_choice, multi_choice
        self.label = field_data.get('label', '')
        self.description = field_data.get('description', '')
        self.placeholder = field_data.get('placeholder', '')
        self.required = field_data.get('required', False)
        self.options = field_data.get('options', [])
        self.validation = field_data.get('validation', {})
        self.value = None


class FormSystem:
    """Interactive form system for console-based input collection."""
    
    def __init__(self):
        self.menu = Menu(title="Form")
        self.results = {}
    
    def load_form(self, form_json: str) -> Dict[str, Any]:
        """Load form definition from JSON string."""
        return json.loads(form_json)
    
    def load_form_from_file(self, file_path: str) -> Dict[str, Any]:
        """Load form definition from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _validate_text(self, value: str, field: FormField) -> tuple[bool, str]:
        """Validate text input."""
        if not value and field.required:
            return False, "此字段为必填项"
        
        validation = field.validation
        
        if value:
            if 'minLength' in validation and len(value) < validation['minLength']:
                return False, f"最小长度为 {validation['minLength']} 个字符"
            
            if 'maxLength' in validation and len(value) > validation['maxLength']:
                return False, f"最大长度为 {validation['maxLength']} 个字符"
            
            if 'pattern' in validation:
                import re
                if not re.match(validation['pattern'], value):
                    return False, validation.get('errorMessage', '输入格式不正确')
        
        return True, ""
    
    def _get_text_input(self, field: FormField, field_num: int, total_fields: int) -> Optional[str]:
        """Get text input from user."""
        print(f"\n[{field_num}/{total_fields}] {field.label}")
        if field.description:
            print(f"    {field.description}")
        if field.placeholder:
            print(f"    (例如: {field.placeholder})")
        if not field.required:
            print(f"    (可选，按 ENTER 跳过)")
        
        while True:
            user_input = input("➤ ").strip()
            
            # 如果是可选字段且用户按ENTER，跳过
            if not user_input and not field.required:
                return None
            
            # 验证输入
            is_valid, error_msg = self._validate_text(user_input, field)
            if not is_valid:
                print(f"❌ {error_msg}")
                continue
            
            return user_input if user_input else None
    
    def _get_single_choice(self, field: FormField, field_num: int, total_fields: int) -> Optional[str]:
        """Get single choice selection from user."""
        print(f"\n[{field_num}/{total_fields}] {field.label}")
        if field.description:
            print(f"    {field.description}")
        print(f"    (使用 ↑↓ 箭头键选择，ENTER 确认)")
        
        if not field.options:
            print("❌ 没有可用的选项")
            return None
        
        selected_idx = 0
        
        while True:
            # 显示选项
            print()
            for i, option in enumerate(field.options):
                if i == selected_idx:
                    # 高亮选中的选项
                    print(f"  ● {option['label']}")
                else:
                    print(f"    {option['label']}")
            
            # 获取用户输入
            key = self._get_key()
            
            if key == 'up':
                selected_idx = (selected_idx - 1) % len(field.options)
                # 清除之前的输出，重新显示
                self._clear_lines(len(field.options) + 1)
            elif key == 'down':
                selected_idx = (selected_idx + 1) % len(field.options)
                # 清除之前的输出，重新显示
                self._clear_lines(len(field.options) + 1)
            elif key == 'enter':
                selected_value = field.options[selected_idx]['value']
                print(f"✓ 已选择: {field.options[selected_idx]['label']}")
                return selected_value
            elif key == 'esc':
                print("⊘ 已取消")
                return None
    
    def _get_multi_choice(self, field: FormField, field_num: int, total_fields: int) -> Optional[List[str]]:
        """Get multiple choice selections from user."""
        print(f"\n[{field_num}/{total_fields}] {field.label}")
        if field.description:
            print(f"    {field.description}")
        print(f"    (使用 ↑↓ 箭头键导航，SPACE 切换选择，ENTER 确认)")
        
        if not field.options:
            print("❌ 没有可用的选项")
            return None
        
        selected_indices = set()
        current_idx = 0
        
        while True:
            # 显示选项
            print()
            for i, option in enumerate(field.options):
                checkbox = "☑️" if i in selected_indices else "☐"
                if i == current_idx:
                    # 高亮当前选项
                    print(f"  ► {checkbox} {option['label']}")
                else:
                    print(f"    {checkbox} {option['label']}")
            
            # 显示已选择数量
            selected_count = len(selected_indices)
            print(f"\n  已选择: {selected_count} 项")
            
            # 获取用户输入
            key = self._get_key()
            
            if key == 'up':
                current_idx = (current_idx - 1) % len(field.options)
                # 清除之前的输出，重新显示
                self._clear_lines(len(field.options) + 3)
            elif key == 'down':
                current_idx = (current_idx + 1) % len(field.options)
                # 清除之前的输出，重新显示
                self._clear_lines(len(field.options) + 3)
            elif key == 'space':
                # 切换选择
                if current_idx in selected_indices:
                    selected_indices.remove(current_idx)
                else:
                    selected_indices.add(current_idx)
                # 清除之前的输出，重新显示
                self._clear_lines(len(field.options) + 3)
            elif key == 'enter':
                selected_values = [field.options[i]['value'] for i in sorted(selected_indices)]
                selected_labels = [field.options[i]['label'] for i in sorted(selected_indices)]
                if selected_values:
                    print(f"\n✓ 已选择 {len(selected_values)} 项:")
                    for label in selected_labels:
                        print(f"    • {label}")
                else:
                    print(f"\n✓ 未选择任何项")
                return selected_values if selected_values else []
            elif key == 'esc':
                print("⊘ 已取消")
                return None
    
    def _get_key(self) -> str:
        """Get key input from user (Windows/Unix compatible)."""
        import sys
        
        if sys.platform == 'win32':
            import msvcrt
            key = msvcrt.getch()
            
            if key == b'\x00' or key == b'\xe0':  # Special keys
                key = msvcrt.getch()
                if key == b'H':  # Up arrow
                    return 'up'
                elif key == b'P':  # Down arrow
                    return 'down'
                elif key == b'K':  # Left arrow
                    return 'left'
                elif key == b'M':  # Right arrow
                    return 'right'
                return 'unknown'
            elif key == b'\r':  # Enter
                return 'enter'
            elif key == b' ':  # Space
                return 'space'
            elif key == b'\x1b':  # Escape
                return 'esc'
            else:
                return 'unknown'
        else:
            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                key = sys.stdin.read(1)
                
                if key == '\x1b':  # Escape sequence
                    next_chars = sys.stdin.read(2)
                    if next_chars == '[A':
                        return 'up'
                    elif next_chars == '[B':
                        return 'down'
                    elif next_chars == '[C':
                        return 'right'
                    elif next_chars == '[D':
                        return 'left'
                    return 'esc'
                elif key == '\r' or key == '\n':
                    return 'enter'
                elif key == ' ':
                    return 'space'
                else:
                    return 'unknown'
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def _clear_lines(self, num_lines: int) -> None:
        """Clear previous lines from console."""
        import sys
        for _ in range(num_lines):
            sys.stdout.write('\033[1A')  # Move cursor up
            sys.stdout.write('\033[K')   # Clear line
    
    def process_form(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process form and collect user input."""
        print("\n" + "="*60)
        print(f"  {form_data.get('icon', '📝')} {form_data.get('title', '表单')}")
        print("="*60)
        if form_data.get('description'):
            print(f"\n{form_data['description']}\n")
        
        fields = form_data.get('fields', [])
        self.results = {}
        
        for idx, field_data in enumerate(fields, 1):
            field = FormField(field_data)
            
            if field.type == 'text':
                value = self._get_text_input(field, idx, len(fields))
                self.results[field.id] = value
            
            elif field.type == 'single_choice':
                value = self._get_single_choice(field, idx, len(fields))
                self.results[field.id] = value
            
            elif field.type == 'multi_choice':
                value = self._get_multi_choice(field, idx, len(fields))
                self.results[field.id] = value
        
        return self._format_results(form_data, self.results)
    
    def _format_results(self, form_data: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Format collected results with field information."""
        output = {
            'form_id': form_data.get('id', ''),
            'form_title': form_data.get('title', ''),
            'timestamp': self._get_timestamp(),
            'data': {}
        }
        
        fields_map = {f['id']: f for f in form_data.get('fields', [])}
        
        for field_id, value in results.items():
            if field_id in fields_map:
                field_info = fields_map[field_id]
                output['data'][field_id] = {
                    'label': field_info.get('label', ''),
                    'type': field_info.get('type', ''),
                    'value': value
                }
        
        return output
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def save_results(self, results: Dict[str, Any], file_path: str) -> None:
        """Save results to JSON file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✓ 结果已保存到: {file_path}")
    
    def print_results(self, results: Dict[str, Any]) -> None:
        """Print results in formatted way."""
        print("\n" + "="*60)
        print("  表单提交结果")
        print("="*60)
        print(f"\n表单: {results.get('form_title', '')}")
        print(f"时间: {results.get('timestamp', '')}\n")
        
        for field_id, field_data in results.get('data', {}).items():
            label = field_data.get('label', '')
            value = field_data.get('value', '')
            
            if isinstance(value, list):
                print(f"{label}:")
                if value:
                    for item in value:
                        print(f"  • {item}")
                else:
                    print(f"  (未选择)")
            else:
                print(f"{label}: {value if value else '(未填写)'}")
        
        print("\n" + "="*60)
