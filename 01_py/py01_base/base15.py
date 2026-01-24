#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/11 16:07
# Module    : base15.py
# explain   : 模块 与 包
# 一个模块(module)就是一个py文件(如: base15_moudle.py)
# 而一个包(package)则是一个带有__init__.py文件的文件夹(如: base15_1), 该py文件会定义该模块会暴露哪些变量或函数
# 包是整合多个模块的,即一个包下有多个模块,包通过__init__.py暴露这个包允许被访问的内容,包是一个组织模块的目录
# 必须要有 __init__.py 文件才能让 Python 将包含该文件的目录当作包来处理。

"""
模块的分类
1、内置模块，如os，time等等
2、第三方模块，使用pip或conda等安装的包
3、自定义模块，即在本项目中定义的


# 导入模块的方式
1、将某个模块的所有内容导入：import 模块名
2、导入某个模块的指定内容：form 模块名 import 变量/函数
2、导入某个模块的所有内容：form 模块名 import *
import os
from os import getenv
from os import *

"import 模块名"和”form 模块名 import *“的区别是什么
    方式1：import 模块名：导入模块对象本身，通过 模块名.xxx 访问
    方式3：from 模块名 import *：把模块里的“公共名字”直接拷贝到当前命名空间,这种方式会导入所有不以下划线（_）开头的名称
方式1不会污染当前的命名空间，而方式3会污染当前的命名空间
因此，实战中不要使用方式3

# 通过 as 给导入进来的模块起一个别名，后续就可以通过别名来调用对应的模块
import numpy as np
import pandas as pd


# 使用导入的模块
    模块名.功能名称

# 在模块内部(在任意一个py文件中)可以使用__name__来获取这个模块名
当前文件被直接运行 → __name__ == "__main__"
当前文件被 import → __name__ == 模块名

注意:随着当前模块被导入的方式(位置)不同__name__返回的内容也不固定,但是可以知道的是,如果当前文件直接被执行__name__返回的内容一定是"__main__"
因此不可用 elif 来判断, 只能使用 if ... else ...

此外,如果当前文件被直接运行,那么当前文件的__name__则为"__main__"
因此很多时候,通过 if __name__ == "__main__" 来判断是否为程序入口
# 用来控制py文件在不同应用场景执行不同的逻辑
if __name__ == "__main__":
    # 当前py文件被直接运行
else:
    # 当前py文件被其他模块导入使用要执行的模块初始化代码

# 当py解释器遇到 import base15_1 时,py接收器会执行 base15_1 里面的所有语句,

# 想要知道某个模块都暴露了,哪些东西,可以使用 dir() 内置函数来查看

# 在导入包时,会首先执行改包下的__init__.py文件来对改包进行初始化
__init__.py 文件中不得写,业务或功能代码
__init__.py 是包的入口，用来定义包的边界和初始化，而不是实现具体业务。
1️⃣ 标识目录是 Python 包
2️⃣ 控制包对外暴露的 API
3️⃣ 包级初始化和元信息

"""

# base15.py:  __main__
print("base15.py: ", __name__)

import base15_1
import base15_moudle

print(base15_1.__doc__)
print(base15_1.name)
print(base15_1.base15_1_1_name)
print(base15_1.__version__)
print(base15_1.__author__)
base15_1.say_hello()
base15_1.study()

print(base15_moudle.__doc__)
base15_moudle.work()

# 查看 base15_1 暴露了哪些东西
# ['__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'base15_1', 'name', 'say_hello']
print(dir(base15_1))
print(base15_1.__all__)  # __all__里面输出的列表即为用户暴露的,其他则为系统默认暴露的
print(base15_1.__doc__)
print(base15_1.__file__)
print(base15_1.__name__)
print(base15_1.__package__)
print(base15_1.__path__)
print(base15_1.base15_1)
