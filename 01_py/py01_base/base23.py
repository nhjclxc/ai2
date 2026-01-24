#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/24 18:40
# Module    : base23.py
# explain   : sys模块，https://docs.python.org/zh-cn/3.10/library/sys.html

# os模块负责程序和操作系统进行交互
# sys模块负责和py解释器进行交互

# import sys
import sys

# 获取解释器环境遍历路径
print(sys.path)

# 获取系统编码格式
print(sys.getdefaultencoding())

# 获取操作系统平台名称
print(sys.platform)

# 获取py解释器版本
print(sys.version)
