"""
Interactive Form System for Console
Process form JSON and collect user input interactively.

Supports two modes:
- interactive: Process each field with immediate callback to handler
- submit: Collect all fields and submit to endpoint as JSON
"""
import json
from typing import Any, Dict, List, Optional, Callable
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
    """
    Interactive form system for console-based input collection.
    
    Supports two modes:
    - 'interactive': Process each field and immediately invoke callback on handler object
    - 'submit': Collect all fields, validate, generate JSON and submit to endpoint
    """
    
    def __init__(self, mode: str = 'submit', handler: Optional[Any] = None, endpoint: Optional[str] = None, pre_validation_handler: Optional[Any] = None):
        """
        Initialize FormSystem.
        
        Args:
            mode: 'interactive' or 'submit' (default: 'submit')
            handler: Handler object with callback methods (required for interactive mode)
            endpoint: API endpoint URL (optional for submit mode, can handle JSON generation only)
            pre_validation_handler: Handler object with pre-validation methods (optional)
        """
        self.mode = mode  # 'interactive' or 'submit'
        self.handler = handler
        self.pre_validation_handler = pre_validation_handler
        self.endpoint = endpoint
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
        # Display field with full prompts
        print(f"\n[{field_num}/{total_fields}] {field.label}")
        if field.description:
            print(f"    {field.description}")
        if field.placeholder:
            print(f"    (例如: {field.placeholder})")
        if not field.required:
            print(f"    (可选，按 ENTER 跳过)")
        
        # Check for pre-validation
        pre_validated_value = self._check_pre_validation(field)
        if pre_validated_value is not None:
            print(f"    (预设值: {pre_validated_value})")
            use_existing = self._confirm_use_existing_value(pre_validated_value)
            if use_existing:
                return pre_validated_value
        
        try:
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
        except KeyboardInterrupt:
            raise
    
    def _get_text_input_dynamic(self, field: FormField, field_num: int, total_fields: int) -> Optional[str]:
        """Get text input from user with dynamic UI updates."""
        # Check for pre-validation
        pre_validated_value = self._check_pre_validation(field)
        if pre_validated_value is not None:
            print(f"    (预设值: {pre_validated_value})")
            use_existing = self._confirm_use_existing_value(pre_validated_value)
            if use_existing:
                print(f"[{field_num}/{total_fields}] {field.label}: {pre_validated_value}")
                return pre_validated_value
        
        # Track the number of lines printed for this field
        lines_printed = 2  # Start with the blank line and field header line: "\n[1/6] Field Name"
        
        # Show full field information
        print(f"\n[{field_num}/{total_fields}] {field.label}")
        if field.description:
            print(f"    {field.description}")
            lines_printed += 1
        if field.placeholder:
            print(f"    (例如: {field.placeholder})")
            lines_printed += 1
        if not field.required:
            print(f"    (可选，按 ENTER 跳过)")
            lines_printed += 1
        
        try:
            while True:
                user_input = input("➤ ").strip()
                
                # 如果是可选字段且用户按ENTER，跳过
                if not user_input and not field.required:
                    # Clear all lines for this field and show the result
                    import sys
                    for _ in range(lines_printed):
                        sys.stdout.write('\033[1A\033[2K')  # Move up and clear line
                    print(f"[{field_num}/{total_fields}] {field.label}: (skipped)")
                    return None
                
                # 验证输入
                is_valid, error_msg = self._validate_text(user_input, field)
                if not is_valid:
                    print(f"❌ {error_msg}")
                    lines_printed += 1  # Account for error message
                    continue
                
                # Clear all lines for this field and show the result
                import sys
                for _ in range(lines_printed):
                    sys.stdout.write('\033[1A\033[2K')  # Move up and clear line
                result = user_input if user_input else None
                print(f"[{field_num}/{total_fields}] {field.label}: {result}")
                return result
        except KeyboardInterrupt:
            raise
    
    def _get_single_choice(self, field: FormField, field_num: int, total_fields: int) -> Optional[str]:
        """Get single choice selection from user."""
        print(f"\n[{field_num}/{total_fields}] {field.label}")
        if field.description:
            print(f"    {field.description}")
        print(f"    (使用 ↑↓ 箭头键选择，ENTER 确认)")
        
        # Check for pre-validation
        pre_validated_value = self._check_pre_validation(field)
        if pre_validated_value is not None:
            # Find the option that matches the pre-validated value
            matching_option = None
            for option in field.options:
                if option['value'] == pre_validated_value:
                    matching_option = option
                    break
            if matching_option:
                print(f"    (预设值: {matching_option['label']})")
                use_existing = self._confirm_use_existing_value(matching_option['label'])
                if use_existing:
                    return pre_validated_value
        
        if not field.options:
            print("❌ 没有可用的选项")
            return None
        
        selected_idx = 0
        
        try:
            show_options = True  # 标记是否需要显示选项
            while True:
                # 根据标记决定是否显示选项
                if show_options:
                    print()
                    for i, option in enumerate(field.options):
                        if i == selected_idx:
                            # 高亮选中的选项
                            print(f"  ● {option['label']}")
                        else:
                            print(f"    {option['label']}")
                
                # 重置标记，等待按键处理决定是否需要重新显示
                show_options = False
                
                # 获取用户输入
                key = self._get_key()
                
                if key == 'up':
                    selected_idx = (selected_idx - 1) % len(field.options)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 1)
                    show_options = True  # 需要重新显示选项
                elif key == 'down':
                    selected_idx = (selected_idx + 1) % len(field.options)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 1)
                    show_options = True  # 需要重新显示选项
                elif key == 'left' or key == 'right':
                    # Treat left/right like up/down for single select
                    if key == 'left':
                        selected_idx = (selected_idx - 1) % len(field.options)
                    else:  # key == 'right'
                        selected_idx = (selected_idx + 1) % len(field.options)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 1)
                    show_options = True  # 需要重新显示选项
                elif key == 'enter':
                    selected_value = field.options[selected_idx]['value']
                    print(f"✓ 已选择: {field.options[selected_idx]['label']}")
                    return selected_value
                elif key == 'esc':
                    print("⊘ 已取消")
                    return None
                # 对于无效按键（包括 'space'、'unknown' 等），show_options 保持 False
                # 这样下次循环就不会重新显示选项
        except KeyboardInterrupt:
            raise
    
    def _get_single_choice_dynamic(self, field: FormField, field_num: int, total_fields: int) -> Optional[str]:
        """Get single choice selection from user with dynamic UI updates."""
        # Check for pre-validation
        pre_validated_value = self._check_pre_validation(field)
        if pre_validated_value is not None:
            # Find the option that matches the pre-validated value
            matching_option = None
            for option in field.options:
                if option['value'] == pre_validated_value:
                    matching_option = option
                    break
            if matching_option:
                print(f"    (预设值: {matching_option['label']})")
                use_existing = self._confirm_use_existing_value(matching_option['label'])
                if use_existing:
                    print(f"[{field_num}/{total_fields}] {field.label}: {matching_option['label']}")
                    return pre_validated_value
        
        if not field.options:
            print("❌ 没有可用的选项")
            return None
        
        selected_idx = 0
        
        # Track the number of lines printed for this field
        lines_printed = 2  # Start with the blank line and field header line: "\n[1/6] Field Name"
        if field.description:
            lines_printed += 1
        #lines_printed += 1  # Instruction line: "(使用 ↑↓ 箭头键选择，ENTER 确认)"
        lines_printed += len(field.options)  # All the options
        lines_printed += 1  # Blank line before options
        
        try:
            # Show full field information
            print(f"\n[{field_num}/{total_fields}] {field.label}")
            if field.description:
                print(f"    {field.description}")
            print(f"    (使用 ↑↓ 箭头键选择，ENTER 确认)")
            
            show_options = True  # 标记是否需要显示选项
            while True:
                # 根据标记决定是否显示选项
                if show_options:
                    # 显示选项
                    print()
                    for i, option in enumerate(field.options):
                        if i == selected_idx:
                            # 高亮选中的选项
                            print(f"  ● {option['label']}")
                        else:
                            print(f"    {option['label']}")
                
                # 重置标记，等待按键处理决定是否需要重新显示
                show_options = False
                
                # 获取用户输入
                key = self._get_key()
                
                if key == 'up':
                    selected_idx = (selected_idx - 1) % len(field.options)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 1)
                    show_options = True  # 需要重新显示选项
                elif key == 'down':
                    selected_idx = (selected_idx + 1) % len(field.options)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 1)
                    show_options = True  # 需要重新显示选项
                elif key == 'left' or key == 'right':
                    # Treat left/right like up/down for single select
                    if key == 'left':
                        selected_idx = (selected_idx - 1) % len(field.options)
                    else:  # key == 'right'
                        selected_idx = (selected_idx + 1) % len(field.options)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 1)
                    show_options = True  # 需要重新显示选项
                elif key == 'enter':
                    selected_value = field.options[selected_idx]['value']
                    selected_label = field.options[selected_idx]['label']
                    # Clear all lines for this field and show the result
                    import sys
                    for _ in range(lines_printed):
                        sys.stdout.write('\033[1A\033[2K')
                    print(f"[{field_num}/{total_fields}] {field.label}: {selected_label}")
                    return selected_value
                elif key == 'esc':
                    print("⊘ 已取消")
                    # Clear all lines for this field
                    import sys
                    for _ in range(lines_printed):
                        sys.stdout.write('\033[1A\033[2K')
                    return None
                # 对于无效按键（包括 'space'、'unknown' 等），show_options 保持 False
                # 这样下次循环就不会重新显示选项
        except KeyboardInterrupt:
            raise
    
    def _get_multi_choice(self, field: FormField, field_num: int, total_fields: int) -> Optional[List[str]]:
        """Get multiple choice selections from user."""
        print(f"\n[{field_num}/{total_fields}] {field.label}")
        if field.description:
            print(f"    {field.description}")
        print(f"    (使用 ↑↓ 箭头键导航，SPACE 切换选择，ENTER 确认)")
        
        # Check for pre-validation
        pre_validated_value = self._check_pre_validation(field)
        if pre_validated_value is not None and isinstance(pre_validated_value, list):
            # Find the options that match the pre-validated values
            matching_options = []
            for option in field.options:
                if option['value'] in pre_validated_value:
                    matching_options.append(option['label'])
            
            if matching_options:
                print(f"    (预设值: {', '.join(matching_options)})")
                use_existing = self._confirm_use_existing_value(', '.join(matching_options))
                if use_existing:
                    return pre_validated_value
        
        if not field.options:
            print("❌ 没有可用的选项")
            return None
        
        selected_indices = set()
        current_idx = 0
        
        try:
            show_options = True  # 标记是否需要显示选项
            while True:
                # 根据标记决定是否显示选项
                if show_options:
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
                
                # 重置标记，等待按键处理决定是否需要重新显示
                show_options = False
                
                # 获取用户输入
                key = self._get_key()
                
                if key == 'up':
                    current_idx = (current_idx - 1) % len(field.options)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 3)
                    show_options = True  # 需要重新显示选项
                elif key == 'down':
                    current_idx = (current_idx + 1) % len(field.options)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 3)
                    show_options = True  # 需要重新显示选项
                elif key == 'left' or key == 'right':
                    # Treat left/right like up/down for multi-select navigation
                    if key == 'left':
                        current_idx = (current_idx - 1) % len(field.options)
                    else:  # key == 'right'
                        current_idx = (current_idx + 1) % len(field.options)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 3)
                    show_options = True  # 需要重新显示选项
                elif key == 'space':
                    # 切换选择
                    if current_idx in selected_indices:
                        selected_indices.remove(current_idx)
                    else:
                        selected_indices.add(current_idx)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 3)
                    show_options = True  # 需要重新显示选项
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
                # 对于无效按键（包括 'unknown' 等），show_options 保持 False
                # 这样下次循环就不会重新显示选项
        except KeyboardInterrupt:
            raise
    
    def _get_multi_choice_dynamic(self, field: FormField, field_num: int, total_fields: int) -> Optional[List[str]]:
        """Get multiple choice selections from user with dynamic UI updates."""
        # Check for pre-validation
        pre_validated_value = self._check_pre_validation(field)
        if pre_validated_value is not None and isinstance(pre_validated_value, list):
            # Find the options that match the pre-validated values
            matching_options = []
            for option in field.options:
                if option['value'] in pre_validated_value:
                    matching_options.append(option['label'])
            
            if matching_options:
                print(f"    (预设值: {', '.join(matching_options)})")
                use_existing = self._confirm_use_existing_value(', '.join(matching_options))
                if use_existing:
                    print(f"[{field_num}/{total_fields}] {field.label}: {', '.join(matching_options)}")
                    return pre_validated_value
        
        if not field.options:
            print("❌ 没有可用的选项")
            return None
        
        selected_indices = set()
        current_idx = 0
        
        # Track the number of lines printed for this field
        lines_printed = 2  # Start with the blank line and field header line: "\n[1/6] Field Name"
        if field.description:
            lines_printed += 1
        lines_printed += 1  # Instruction line: "(使用 ↑↓ 箭头键导航，SPACE 切换选择，ENTER 确认)"
        lines_printed += len(field.options)  # All the options
        lines_printed += 2  # Blank line before options and selection count line
        
        try:
            # Show full field information
            print(f"\n[{field_num}/{total_fields}] {field.label}")
            if field.description:
                print(f"    {field.description}")
            print(f"    (使用 ↑↓ 箭头键导航，SPACE 切换选择，ENTER 确认)")
            
            show_options = True  # 标记是否需要显示选项
            while True:
                # 根据标记决定是否显示选项
                if show_options:
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
                
                # 重置标记，等待按键处理决定是否需要重新显示
                show_options = False
                
                # 获取用户输入
                key = self._get_key()
                
                if key == 'up':
                    current_idx = (current_idx - 1) % len(field.options)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 3)
                    show_options = True  # 需要重新显示选项
                elif key == 'down':
                    current_idx = (current_idx + 1) % len(field.options)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 3)
                    show_options = True  # 需要重新显示选项
                elif key == 'left' or key == 'right':
                    # Treat left/right like up/down for multi-select navigation
                    if key == 'left':
                        current_idx = (current_idx - 1) % len(field.options)
                    else:  # key == 'right'
                        current_idx = (current_idx + 1) % len(field.options)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 3)
                    show_options = True  # 需要重新显示选项
                elif key == 'space':
                    # 切换选择
                    if current_idx in selected_indices:
                        selected_indices.remove(current_idx)
                    else:
                        selected_indices.add(current_idx)
                    # 清除之前的输出，重新显示
                    self._clear_lines(len(field.options) + 3)
                    show_options = True  # 需要重新显示选项
                elif key == 'enter':
                    selected_values = [field.options[i]['value'] for i in sorted(selected_indices)]
                    selected_labels = [field.options[i]['label'] for i in sorted(selected_indices)]
                    
                    # Clear all lines for this field and show the result
                    import sys
                    for _ in range(lines_printed):
                        sys.stdout.write('\033[1A\033[2K')
                    
                    # Print the completed field in the desired format
                    if selected_values:
                        result_str = ', '.join(selected_labels)
                        print(f"[{field_num}/{total_fields}] {field.label}: {result_str}")
                    else:
                        print(f"[{field_num}/{total_fields}] {field.label}: (no selection)")
                    
                    return selected_values if selected_values else []
                elif key == 'esc':
                    print("⊘ 已取消")
                    # Clear all lines for this field
                    import sys
                    for _ in range(lines_printed):
                        sys.stdout.write('\033[1A\033[2K')
                    return None
                # 对于无效按键（包括 'unknown' 等），show_options 保持 False
                # 这样下次循环就不会重新显示选项
        except KeyboardInterrupt:
            raise
    
    def _get_key(self) -> str:
        """Get key input from user (Windows/Unix compatible)."""
        import sys
        
        if sys.platform == 'win32':
            import msvcrt
            key = msvcrt.getch()
            
            if key == b'\x03':  # Ctrl+C
                raise KeyboardInterrupt()
            elif key == b'\x00' or key == b'\xe0':  # Special keys
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
                
                if key == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt()
                elif key == '\x1b':  # Escape sequence
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
    
    def _check_pre_validation(self, field: FormField) -> Optional[Any]:
        """
        Check if there's a pre-validation handler for this field.
        
        Args:
            field: The field to check for pre-validation
            
        Returns:
            Pre-validated value if available, None otherwise
        """
        if not self.pre_validation_handler:
            return None
        
        # Construct callback method name
        callback_name = f'pre_validate_{field.id}'
        
        if hasattr(self.pre_validation_handler, callback_name):
            callback_method = getattr(self.pre_validation_handler, callback_name)
            try:
                # Pass the current results so far to the pre-validation handler
                return callback_method(field, self.results)
            except Exception as e:
                print(f"❌ Error in pre-validation for field '{field.id}': {str(e)}")
                return None
        else:
            return None
    
    def _confirm_use_existing_value(self, value_display: str) -> bool:
        """
        Ask user whether to use an existing/pre-validated value.
        
        Args:
            value_display: String representation of the existing value
            
        Returns:
            True if user wants to use the existing value, False otherwise
        """
        try:
            # Use the existing yes_no_prompt functionality
            confirmation = self.menu.yes_no_prompt(
                question=f"Use existing value: {value_display}?",
                description="Press LEFT/RIGHT to select, ENTER to confirm"
            )
            return confirmation is True
        except KeyboardInterrupt:
            raise
    
    def _print_completed_field(self, idx: int, total: int, label: str, value: Any, field_type: str, options: List[Dict]) -> None:
        """
        Print a completed field in the format [1/6] Full Name: Kenny
        
        Args:
            idx: Current field index
            total: Total number of fields
            label: Field label
            value: Field value
            field_type: Type of the field ('text', 'single_choice', 'multi_choice')
            options: List of options for choice fields
        """
        if value is not None:
            # Format the value based on field type
            if field_type == 'multi_choice' and isinstance(value, list):
                # For multi-choice, show selected options
                if value:
                    # Find the labels for the selected values
                    selected_labels = []
                    for opt in options:
                        if opt.get('value') in value:
                            selected_labels.append(opt.get('label', opt.get('value')))
                    value_str = ", ".join(selected_labels) if selected_labels else str(value)
                else:
                    value_str = "(no selection)"
            elif field_type == 'single_choice':
                # For single choice, find the label for the selected value
                value_str = str(value)
                for opt in options:
                    if opt.get('value') == value:
                        value_str = opt.get('label', value)
                        break
            else:
                # For text and other types
                value_str = str(value)
            
            print(f"[{idx}/{total}] {label}: {value_str}")
        else:
            print(f"[{idx}/{total}] {label}")
    
    def process_form(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process form and collect user input with dynamic UI.
        
        In 'interactive' mode: Calls handler callbacks after each field is collected.
        In 'submit' mode: Collects all fields and returns formatted results (no immediate processing).
        """
        try:
            # Print initial form header
            print("\n" + "="*60)
            print(f"  {form_data.get('icon', '📝')} {form_data.get('title', '表单')}")
            print("="*60)
            if form_data.get('description'):
                print(f"\n{form_data['description']}\n")
            
            fields = form_data.get('fields', [])
            self.results = {}
            
            # Process each field with dynamic UI updates
            for idx, field_data in enumerate(fields, 1):
                field = FormField(field_data)
                
                # Collect field value with dynamic display
                if field.type == 'text':
                    value = self._get_text_input_dynamic(field, idx, len(fields))
                    self.results[field.id] = value
                
                elif field.type == 'single_choice':
                    value = self._get_single_choice_dynamic(field, idx, len(fields))
                    self.results[field.id] = value
                
                elif field.type == 'multi_choice':
                    value = self._get_multi_choice_dynamic(field, idx, len(fields))
                    self.results[field.id] = value
                
                # In interactive mode, invoke handler callback immediately after field collection
                if self.mode == 'interactive':
                    self._invoke_field_handler(field.id, self.results[field.id], field)
            
            # Format and return results
            return self._format_results(form_data, self.results)
            
        except KeyboardInterrupt:
            print("\n\n" + "="*60)
            print("  ⏹️  表单已取消")
            print("="*60 + "\n")
            return None
    
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
        
        # In submit mode, automatically submit the results
        if self.mode == 'submit':
            self._submit_results(output)
        
        return output
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _invoke_field_handler(self, field_id: str, field_value: Any, field: FormField) -> None:
        """
        Invoke handler callback for a field (interactive mode).
        
        Expects handler to have a method: on_field_<field_id>(value, field)
        For example: on_field_name(value, field) for field_id='name'
        """
        if not self.handler:
            return
        
        # Construct callback method name
        callback_name = f'on_field_{field_id}'
        
        if hasattr(self.handler, callback_name):
            callback_method = getattr(self.handler, callback_name)
            try:
                callback_method(field_value, field)
                print(f"✓ Field '{field_id}' processed successfully")
            except Exception as e:
                print(f"❌ Error processing field '{field_id}': {str(e)}")
        else:
            # Optional: Log if callback method not found
            pass
    
    def _submit_results(self, results: Dict[str, Any]) -> None:
        """
        Submit results to endpoint (submit mode).
        
        If endpoint is provided, sends JSON data via POST request.
        Otherwise, just logs the submission.
        """
        if not self.endpoint:
            print(f"\n✓ Form data prepared for submission (no endpoint configured)")
            return
        
        try:
            import requests
            
            print(f"\n📤 Submitting form data to {self.endpoint}...")
            
            response = requests.post(
                self.endpoint,
                json=results,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [200, 201, 202]:
                print(f"✓ Form submitted successfully")
                if response.text:
                    print(f"Response: {response.text}")
            else:
                print(f"❌ Submission failed with status {response.status_code}")
                print(f"Response: {response.text}")
        except ImportError:
            print(f"⚠️  requests library not available. Set up HTTP client to submit.")
        except Exception as e:
            print(f"❌ Error submitting form: {str(e)}")
    
    def save_results(self, results: Dict[str, Any], file_path: str) -> None:
        """Save results to JSON file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✓ 结果已保存到: {file_path}")
    
    def print_results(self, results: Dict[str, Any]) -> None:
        """Print results in OpenClaw-style formatted way."""
        width = 82
        border_h = "─" * (width - 2)
        
        def pad_line(text, indent=2):
            """Pad text to fit within the border."""
            padding = width - len(text) - indent - 1
            return text + (" " * max(0, padding))
        
        # Header
        print(f"\n┌{border_h}╮")
        print(f"│{pad_line(' ✓ Form Submission Results', 1)}│")
        print(f"├{border_h}┤")
        
        # Form info
        form_title = results.get('form_title', '')
        timestamp = results.get('timestamp', '')
        print(f"│{pad_line(f'  📋 {form_title}', 1)}│")
        print(f"│{pad_line(f'  🕐 {timestamp}', 1)}│")
        print(f"├{border_h}┤")
        
        # Data section header
        print(f"│{pad_line('  Field Values', 1)}│")
        print(f"├{border_h}┤")
        
        # Data entries
        for field_id, field_data in results.get('data', {}).items():
            label = field_data.get('label', '')
            value = field_data.get('value', '')
            
            if isinstance(value, list):
                print(f"│{pad_line(f'  {label}', 1)}│")
                if value:
                    for item in value:
                        print(f"│{pad_line(f'    ✓ {item}', 1)}│")
                else:
                    print(f"│{pad_line('    (no selection)', 1)}│")
            else:
                display_value = value if value else "(empty)"
                print(f"│{pad_line(f'  {label}: {display_value}', 1)}│")
        
        # Footer
        print(f"└{border_h}╯\n")
