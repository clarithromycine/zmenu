# ANSI转义码方案配置指南

## 概述

项目已实现统一的ANSI转义码管理系统，所有ANSI转义码（包括颜色、光标操作、屏幕清除等）都集中在 `ansi_scheme.json` 中配置，通过 `ansi_manager.py` 提供便捷的接口使用。

## 文件说明

### 1. `ansi_scheme.json` - ANSI转义码配置文件

定义了所有ANSI转义码：

```json
{
  "colors": {
    "primary": {
      "code": "\u001b[38;5;208m",
      "name": "orange",
      "description": "Primary highlight color for selected items"
    },
    "secondary": {
      "code": "\u001b[90m",
      "name": "gray",
      "description": "Secondary color for descriptions and hints"
    },
    "reset": {
      "code": "\u001b[0m",
      "name": "reset",
      "description": "Reset all formatting to default"
    }
  },
  "cursor": {
    "hide": "\u001b[?25l",
    "show": "\u001b[?25h"
  },
  "cursor_movement": {
    "up": "\u001b[A",
    "down": "\u001b[B",
    "right": "\u001b[C",
    "left": "\u001b[D"
  },
  "screen": {
    "clear_line": "\u001b[2K",
    "clear_to_end": "\u001b[0J"
  }
}
```

### 2. `ansi_manager.py` - ANSI转义码管理模块

提供了便捷的API接口来使用ANSI转义码配置。

## 使用方法

### 基础使用

```python
from ansi_manager import get_ansi_scheme

# 获取全局ANSI方案实例
ansi = get_ansi_scheme()

# 获取颜色代码
primary_color = ansi.get_color('primary')
secondary_color = ansi.get_color('secondary')
reset_color = ansi.get_color('reset')

# 输出彩色文本
print(f"{primary_color}这是主要颜色{reset_color}")
print(f"{secondary_color}这是次要颜色{reset_color}")
```

### 游标操作

```python
ansi = get_ansi_scheme()

# 隐藏光标
print(ansi.get_cursor('hide'), end='', flush=True)

# 显示光标
print(ansi.get_cursor('show'), end='', flush=True)

# 移动光标（参数：方向、行数）
print(ansi.get_cursor_move('up', 3), end='', flush=True)
print(ansi.get_cursor_move('down', 2), end='', flush=True)
```

### 屏幕操作

```python
ansi = get_ansi_scheme()

# 清除当前行
print(ansi.get_screen('clear_line'), end='', flush=True)

# 清除到屏幕末尾
print(ansi.get_screen('clear_to_end'), end='', flush=True)
```

### 便捷方法

```python
ansi = get_ansi_scheme()

# 给文本添加颜色
highlighted_text = ansi.colorize("重要信息", color='primary')
hint_text = ansi.colorize("提示信息", color='secondary')

# 格式化菜单项
item = ansi.get_highlight_item("菜单项标签", "这是长描述")

# 格式化复选框
checkbox = ansi.get_checkbox_item(True, "已选择", highlighted=True)

# 格式化是/否选择
yes_no = ansi.get_yes_no_text(0)  # 0表示选中YES，1表示选中NO
```

### 初始化自定义配置

```python
from ansi_manager import initialize_ansi_scheme

# 从自定义路径加载配置
ansi = initialize_ansi_scheme('/path/to/custom_ansi_scheme.json')
```

## 修改ANSI配置

要修改应用的整体样式，只需编辑 `ansi_scheme.json` 文件中的ANSI代码：

### 常用的256色ANSI代码

- `\033[38;5;208m` - 橙色（当前主色）
- `\033[38;5;196m` - 红色
- `\033[38;5;46m` - 绿色
- `\033[38;5;33m` - 蓝色
- `\033[38;5;226m` - 黄色
- `\033[38;5;199m` - 紫色
- `\033[90m` - 灰色（当前次色）
- `\033[0m` - 重置（必需）

### 示例：改为绿色主题

编辑 `ansi_scheme.json`：

```json
{
  "colors": {
    "primary": {
      "code": "\u001b[38;5;46m",
      "name": "green",
      "description": "Primary highlight color for selected items"
    },
    // ... 其他配置保持不变
  }
}
```

## 集成在代码中

### 在menu_system.py中

```python
from ansi_manager import get_ansi_scheme

class Menu:
    def _display_items(self, selected_idx: int = 0) -> None:
        ansi = get_ansi_scheme()
        # 使用 ansi.get_color() 来获取颜色代码
        primary = ansi.get_color('primary')
        secondary = ansi.get_color('secondary')
        reset = ansi.get_color('reset')
        # ... 使用ANSI代码
```

### 在form_system.py中

```python
from ansi_manager import get_ansi_scheme

class FormSystem:
    def _get_single_choice(self, field):
        ansi = get_ansi_scheme()
        # 使用ANSI管理器提供的便捷方法
        checkbox = ansi.get_checkbox_item(True, "选项", highlighted=True)
        # ... 使用ANSI代码
```

## 优势

1. **统一管理** - 所有ANSI转义码集中在一个JSON文件中
2. **易于定制** - 修改样式只需编辑JSON文件，无需改动代码
3. **便捷接口** - AnsiScheme提供了丰富的便捷方法
4. **跨平台** - 支持Windows、Linux、macOS
5. **可维护性** - 代码中无硬编码的ANSI代码

## 现有使用

以下模块已集成ANSI管理器：

- ✅ `menu_system.py` - 菜单系统的所有ANSI操作
- ⏳ `form_system.py` - 待集成（可选）
- ⏳ `console_app.py` - 待集成（可选）

## 扩展建议

可以进一步扩展 `ansi_scheme.json` 来支持：

1. 多种主题（亮色/暗色）
2. 错误/警告/成功消息的专用颜色
3. 支持256色或真彩色的不同模式
4. 文本样式（粗体、斜体等）
