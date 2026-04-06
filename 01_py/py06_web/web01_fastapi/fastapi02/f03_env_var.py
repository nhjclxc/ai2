#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/5 15:08
# Module    : f03_env_var.py
# explain   : 环境变量
# explain   : https://fastapi.org.cn/environment-variables/

# 环境变量（也称为“env var”）是存在于 Python 代码之外、位于操作系统中的变量，可以被您的 Python 代码（或其他程序）读取。

# 读取 MY_NAME 环境变量
# 在win的cmd设置环境变量的方式：$env:MY_NAME="lxc123"
# (venv) PS D:\code\py\ai2\01_py\py06_web\web01_fastapi\fastapi01> $env:MY_NAME="lxc123"
# (venv) PS D:\code\py\ai2\01_py\py06_web\web01_fastapi\fastapi01> python f03_env_var.py
# myname_env 读取到的数据: lxc123

import os
# myname_env = os.getenv("MY_NAME")
myname_env = os.getenv("MY_NAME", "somebody")
print(f"myname_env 读取到的数据: {myname_env}")


print("PATH: ", os.getenv("PATH"))

# 注意：os.getenv读取到的数据都是str类型的，在py代码里面可以转化为指定类型
