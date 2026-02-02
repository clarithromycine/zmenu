# MenuItemCmd 参数系统实现总结

## 实现内容

成功添加了参数收集系统到MenuItemCmd装饰器，支持菜单项自动收集用户输入。

### 1. MenuItemCmd 装饰器增强

**新增属性：**
- `params`: 必须参数列表 (List[Dict])
- `options`: 可选参数列表 (List[Dict])

```python
@MenuItemCmd(
    cmd='calc',
    params=[
        {'name': 'num1', 'type': 'number', 'description': 'First number', 'validation_rule': 'required'},
        {'name': 'num2', 'type': 'number', 'description': 'Second number', 'validation_rule': 'required'},
    ],
    options=[
        {'name': 'operation', 'type': 'choice', 'description': 'Operation', 'default': 'add', 'choices': ['add', 'subtract', 'multiply', 'divide']},
    ]
)
def show_calculator(self, params, options):
    # params: {'num1': '10', 'num2': '20'}
    # options: {'operation': 'add'}
    pass
```

### 2. MenuItem 类更新

**变更：**
- 新增 `params` 和 `options` 存储
- `execute()` 方法现在接收 `collected_params` 和 `collected_options` 参数
- 所有函数现在接收 (params, options) 两个参数

```python
def execute(self, collected_params: Dict[str, Any] = None, 
            collected_options: Dict[str, Any] = None) -> bool:
    collected_params = collected_params or {}
    collected_options = collected_options or {}
    return self.action(collected_params, collected_options)
```

### 3. 参数定义格式

#### 参数类型 (params)
```python
{
    'name': 'param_name',           # 参数名 (唯一)
    'type': 'text|number|choice',   # 输入类型
    'description': 'Description',   # 用户提示文本
    'validation_rule': 'rule',      # 验证规则
    'choices': [...]                # choice类型的选项列表
}
```

#### 可选参数 (options)
```python
{
    'name': 'option_name',          # 参数名 (唯一)
    'type': 'text|bool|choice',     # 输入类型
    'description': 'Description',   # 用户提示文本
    'default': 'value',             # 默认值
    'choices': [...]                # choice类型的选项列表
}
```

### 4. 验证规则

支持的验证规则：
- `'required'`: 字段不能为空
- `'min_length:N'`: 最少N个字符
- `'max_length:N'`: 最多N个字符
- `'range:MIN-MAX'`: 数值范围 (仅用于number类型)

### 5. 类型支持

**参数/可选参数类型：**
- `'text'`: 文本输入
- `'number'`: 数值输入
- `'choice'`: 单选列表
- `'bool'` (仅可选参数): 是/否开关

### 6. 核心实现方法

#### Menu._collect_parameters()
自动生成表单并收集用户输入
- 为每个参数创建表单字段
- 为每个可选参数创建表单字段
- 使用FormSystem处理输入
- 返回 (params_dict, options_dict)

#### Menu._create_validator()
根据验证规则创建验证函数
- 支持required, min_length, max_length, range规则
- 返回Callable验证器

#### Menu._execute_choice()
执行菜单项时自动调用参数收集
- 检测MenuItem是否有params/options
- 如有则调用_collect_parameters()
- 将收集到的参数传递给execute()

### 7. 执行流程

1. 用户选择菜单项
2. 系统检查该项是否有params/options定义
3. 如有，自动生成表单提示用户输入
4. 用户填写表单并提交
5. 系统验证输入数据
6. 调用函数，传入 (collected_params, collected_options)
7. 函数执行业务逻辑
8. 返回True/False控制菜单流程

### 8. 循环导入解决

通过延迟导入解决menu_system.py和form_system.py之间的循环依赖：
```python
def _collect_parameters(self, ...):
    # 在方法内部进行导入，而不是在模块顶部
    from form_system import FormSystem, FormField
```

### 9. console_app.py 示例更新

所有菜单项函数已更新为新签名：
- `hello_world(self, params, options)`
- `show_calculator(self, params, options)` - 包含完整的参数定义示例
- `show_system_info(self, params, options)`
- 等等

calc命令是完整的示例，包含：
- 2个必须参数 (num1, num2)
- 1个可选参数 (operation，choice类型)
- 完整的业务逻辑实现

## 文件变更

### menu_system.py
- ✅ 更新MenuItemCmd装饰器支持params和options
- ✅ 更新MenuItem类存储和使用参数
- ✅ 添加_collect_parameters()方法
- ✅ 添加_create_validator()方法
- ✅ 更新_execute_choice()自动调用参数收集
- ✅ 更新add_item()方法签名

### console_app.py
- ✅ 更新所有MenuItemCmd装饰器调用
- ✅ 更新所有函数签名接收(params, options)
- ✅ show_calculator演示了完整的参数系统使用

### form_system.py
- ✅ 无变更 (保持兼容)

## 验证

✅ 所有语法检查通过 (py_compile)
✅ 参数系统测试通过
✅ 循环导入问题解决
✅ 示例代码可运行

## 使用示例

```python
@MenuItemCmd(
    cmd='transfer',
    params=[
        {'name': 'amount', 'type': 'number', 'description': 'Amount', 'validation_rule': 'range:1-10000'},
        {'name': 'recipient', 'type': 'text', 'description': 'Recipient', 'validation_rule': 'required'},
    ],
    options=[
        {'name': 'priority', 'type': 'choice', 'description': 'Priority', 'default': 'normal', 'choices': ['normal', 'express']},
    ]
)
def transfer_funds(self, params, options):
    amount = float(params['amount'])
    recipient = params['recipient']
    priority = options['priority']
    
    print(f"Transferring {amount} to {recipient} with {priority} priority")
    return True
```

当用户选择此菜单项时：
1. 系统自动显示表单要求输入amount和recipient
2. 用户选择priority选项 (或使用默认值normal)
3. 表单验证 amount在1-10000范围内
4. 表单验证 recipient不为空
5. 调用 transfer_funds(self, params, options)
6. 业务逻辑处理转账

## 下一步建议

1. 在form_example.json中测试参数系统
2. 为更复杂的命令添加参数定义
3. 添加自定义验证器支持
4. 考虑添加条件字段 (某个参数值改变时显示/隐藏其他字段)
