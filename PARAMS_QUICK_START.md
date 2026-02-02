# MenuItemCmd 参数系统 - 快速参考指南

## 5分钟快速开始

### 1. 基础使用

```python
from menu_system import MenuItemCmd

@MenuItemCmd(cmd='hello')
def hello(self, params, options):
    print("Hello!")
    return True
```

### 2. 添加必须参数

```python
@MenuItemCmd(
    cmd='greet',
    params=[
        {'name': 'name', 'type': 'text', 'description': 'Your name', 'validation_rule': 'required'}
    ]
)
def greet(self, params, options):
    print(f"Hello {params['name']}!")
    return True
```

### 3. 添加可选参数

```python
@MenuItemCmd(
    cmd='greet',
    params=[
        {'name': 'name', 'type': 'text', 'description': 'Your name', 'validation_rule': 'required'}
    ],
    options=[
        {'name': 'format', 'type': 'choice', 'description': 'Format', 
         'default': 'casual', 'choices': ['casual', 'formal']}
    ]
)
def greet(self, params, options):
    name = params['name']
    fmt = options.get('format', 'casual')
    if fmt == 'formal':
        print(f"Good day, {name}.")
    else:
        print(f"Hey {name}!")
    return True
```

---

## 参数定义参考

### 参数类型

| 类型 | 说明 | 例子 |
|------|------|------|
| `text` | 文本输入 | 名字、邮箱等 |
| `number` | 数值输入 | 金额、年龄等 |
| `choice` | 单选列表 | 操作类型、优先级等 |
| `bool` | 是/否开关 | 仅用于options |

### 验证规则

| 规则 | 说明 | 例子 |
|------|------|------|
| `required` | 字段必填 | 所有必须参数 |
| `min_length:N` | 最小N个字符 | `min_length:3` |
| `max_length:N` | 最多N个字符 | `max_length:50` |
| `range:MIN-MAX` | 数值范围 | `range:1-100` |

---

## 常见模式

### 模式1：简单输入

```python
@MenuItemCmd(
    cmd='search',
    params=[{'name': 'query', 'type': 'text', 'description': 'Search query', 'validation_rule': 'required'}]
)
def search(self, params, options):
    query = params['query']
    # ... 搜索逻辑
    return True
```

### 模式2：数值输入

```python
@MenuItemCmd(
    cmd='transfer',
    params=[{'name': 'amount', 'type': 'number', 'description': 'Amount', 'validation_rule': 'range:1-10000'}]
)
def transfer(self, params, options):
    amount = float(params['amount'])
    # ... 转账逻辑
    return True
```

### 模式3：选择列表

```python
@MenuItemCmd(
    cmd='set_priority',
    params=[{
        'name': 'priority',
        'type': 'choice',
        'description': 'Priority level',
        'choices': ['low', 'medium', 'high', 'critical']
    }]
)
def set_priority(self, params, options):
    priority = params['priority']
    # ... 设置优先级
    return True
```

### 模式4：组合参数和选项

```python
@MenuItemCmd(
    cmd='send_email',
    params=[
        {'name': 'recipient', 'type': 'text', 'description': 'Email address', 'validation_rule': 'required'},
        {'name': 'subject', 'type': 'text', 'description': 'Subject', 'validation_rule': 'required'},
    ],
    options=[
        {'name': 'priority', 'type': 'choice', 'description': 'Priority', 'default': 'normal', 'choices': ['low', 'normal', 'high']},
        {'name': 'draft', 'type': 'bool', 'description': 'Save as draft', 'default': False},
    ]
)
def send_email(self, params, options):
    recipient = params['recipient']
    subject = params['subject']
    priority = options.get('priority', 'normal')
    draft = options.get('draft', False)
    
    if draft:
        print(f"Saved draft: {subject}")
    else:
        print(f"Sending to {recipient}: {subject} (Priority: {priority})")
    return True
```

---

## 访问参数

```python
def my_command(self, params, options):
    # 获取必须参数
    value1 = params['param_name']
    
    # 获取可选参数（带默认值）
    value2 = options.get('option_name', 'default_value')
    
    # 类型转换
    number_value = float(params['number_param'])
    int_value = int(params['integer_param'])
    
    # 布尔选项
    is_enabled = options.get('flag', False)
```

---

## 返回值

```python
def my_command(self, params, options):
    # ...业务逻辑...
    
    # 返回True - 继续显示当前菜单
    return True
    
    # 返回False - 返回上级菜单
    return False
    
    # 其他值 - 视为True
    return None  # 等同于返回True
```

---

## 调试技巧

### 打印参数值

```python
def my_command(self, params, options):
    print(f"Params: {params}")
    print(f"Options: {options}")
    
    for key, value in params.items():
        print(f"  {key} = {value}")
    
    return True
```

### 验证参数

```python
def my_command(self, params, options):
    # 检查参数是否存在
    if 'required_param' not in params:
        print("Missing required parameter")
        return True
    
    # 检查类型
    try:
        amount = float(params['amount'])
    except ValueError:
        print("Invalid amount")
        return True
    
    return True
```

---

## 常见错误

### ❌ 错误1：忘记接收参数

```python
# 错误
@MenuItemCmd(cmd='hello', params=[...])
def hello(self):  # ← 缺少params和options
    return True

# 正确
@MenuItemCmd(cmd='hello', params=[...])
def hello(self, params, options):  # ← 接收参数
    return True
```

### ❌ 错误2：参数名不匹配

```python
# 错误 - 定义的参数名是'name'
@MenuItemCmd(cmd='greet', params=[{'name': 'name', ...}])
def greet(self, params, options):
    print(params['username'])  # ← 应该是'name'
    return True
```

### ❌ 错误3：没有提供choices

```python
# 错误 - choice类型必须有choices
@MenuItemCmd(
    cmd='choose',
    params=[{'name': 'option', 'type': 'choice', 'description': 'Choose'}]  # ← 缺少choices
)
def choose(self, params, options):
    return True

# 正确
@MenuItemCmd(
    cmd='choose',
    params=[{
        'name': 'option',
        'type': 'choice',
        'description': 'Choose',
        'choices': ['A', 'B', 'C']  # ← 提供choices
    }]
)
def choose(self, params, options):
    return True
```

---

## 性能提示

1. **最小化参数数量** - 不要创建太多参数字段
2. **清晰的描述** - 好的描述减少用户困惑
3. **合理的验证** - 使用验证规则减少无效数据
4. **可选参数默认值** - 为常见选项提供合理默认值

---

## 完整示例

```python
from menu_system import MenuItemCmd

class MyApp:
    @MenuItemCmd(
        cmd='calc',
        params=[
            {'name': 'num1', 'type': 'number', 'description': 'First number', 'validation_rule': 'required'},
            {'name': 'num2', 'type': 'number', 'description': 'Second number', 'validation_rule': 'required'},
        ],
        options=[
            {'name': 'op', 'type': 'choice', 'description': 'Operation', 
             'default': 'add', 'choices': ['add', 'sub', 'mul', 'div']},
            {'name': 'show_steps', 'type': 'bool', 'description': 'Show calculation steps', 'default': False},
        ]
    )
    def calculator(self, params, options):
        a = float(params['num1'])
        b = float(params['num2'])
        op = options.get('op', 'add')
        show_steps = options.get('show_steps', False)
        
        operations = {
            'add': lambda x, y: x + y,
            'sub': lambda x, y: x - y,
            'mul': lambda x, y: x * y,
            'div': lambda x, y: x / y if y != 0 else None,
        }
        
        if show_steps:
            print(f"\nCalculating: {a} {op} {b}")
        
        result = operations[op](a, b)
        print(f"Result: {result}")
        
        return True
```

---

更多信息请参考 [PARAMS_IMPLEMENTATION.md](PARAMS_IMPLEMENTATION.md)
