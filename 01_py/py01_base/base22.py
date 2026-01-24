#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/24 17:16
# Module    : base22.py
# explain   : os模块，https://docs.python.org/zh-cn/3.10/library/os.html

# os模块负责程序和操作系统进行交互
# sys模块负责和py解释器进行交互

# import os
# import os.path
import os
import sys

# 返回操作系统类型
print(os.name)
print(sys.version)
print(sys.getdefaultencoding())
print(sys.getfilesystemencoding())

#  $env:NAME="LXC"
# python .\base22.py
print(os.getenv("NAME"))
print(os.getenv("path"))

# os.path.split: 分割给定的路径，将目录和文件名分割出来，以元组的形式返回
tp = os.path.split(os.getcwd())
print(tp)
print(tp[0])
print(tp[1])
# r表示转义字符串
print(os.path.split(r"D:\code\py\ai2\01_py\py01_base\base15_1\base15_1.py"))

# os.path.dirname:获取目录名
# os.path.basename:获取文件名
# os.path.realpath：获取某个文件的绝对路径
print(os.path.dirname(os.path.realpath(__file__)))
print(os.path.basename(os.path.realpath(__file__)))

# os.path.exists(): 判断路径是否存在
print(os.path.exists(r"D:\code\py\ai2\01_py\py01_base\base15_1\base15_1.py"))
print(os.path.exists(r"DDD:\code\py\ai2\01_py\py01_base\base15_1\base15_1.py"))

# os.path.isfile() : 判断路径是否存在，且是“普通文件”
print(os.path.isfile(r"D:\code\py\ai2\01_py\py01_base\base15_1\base15_1.py"))
print(os.path.isfile(r"D:\code\py\ai2\01_py\py01_base\base15_1"))

# os.path.isdir() : 判断路径是否存在，且路径要是目录
print(os.path.isdir(r"D:\code\py\ai2\01_py\py01_base\base15_1\base15_1.py"))
print(os.path.isdir(r"D:\code\py\ai2\01_py\py01_base\base15_1"))

# os.path.abspath() 获取当前路径下的绝对目录
# os.path.isabs  判断是不是绝对路径
print(os.path.abspath(__file__))
print(os.path.isabs(r"D:\code\py\ai2\01_py\py01_base\base22.py"))
print(os.path.isabs(r"ai2\01_py\py01_base\base22.py"))
