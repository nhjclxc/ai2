# 可以在 __init__.py 里面实现这个模块的初始化过程
# __init__.py文件里面最上面的""""""注释将被视为模块注释
"""
__all__ 只对 from 包 import * 生效
👉 不会限制：
    import 包.模块
    from 包.模块 import 私有函数


# 如果某个模块的变量/方法不向往暴露，还想去使用，那么会发生下面的异常
AttributeError: module 'base15_1' has no attribute 'say_hello'

"""

# base15_1前面这个.表示的是导入当前包（current package）里面的内容，务必添加

"""
相对导入:https://docs.python.org/zh-cn/3.10/tutorial/modules.html#intra-package-references
在模块内部相互导入要使用相对导入
| 写法    | 含义    |
| ----- | ----- |
| `.`   | 当前包   |
| `..`  | 上一级包  |
| `...` | 上上一级包 |

模块外部导入当前包则使用绝对导入，即模块名（也就是包名，即文件夹名）

"""
# 1️⃣ 标识目录是 Python 包

# 2️⃣ 控制包对外暴露的 API
from .base15_1 import name, say_hello
from .base15_1_1 import name as base15_1_1_name, study

# 向外暴露本模块可以提供的变量/方法/模块/类等等
# 如果没有 __all__ 向外暴露可用的变量/函数,则会抛出下列异常
# AttributeError: module 'base15_1' has no attribute 'name'
__all__ = ["name", "say_hello", "base15_1_1_name", "study"]

# base15_1.__init__.py:  base15_1
print("base15_1.__init__.py: ", __name__)

# 3️⃣ 包级初始化和元信息
__version__ = "1.0.0"
__author__ = "LXC"

# 可选,包级初始化
