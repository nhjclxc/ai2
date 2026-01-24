#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/11 16:36
# Module    : base15_1.py
# explain   :

name = "base15_1对应的模块名称"


def say_hello(n: str = name):
    print("hello " + n)


"""
在模块内部，如果某个变量/函数，不希望被外部使用，则使用下划线开头来命名

导入所有 不以下划线 _ 开头 的名字
_xxx 默认被视为“内部使用”
"""
_private_name = "这是我的隐藏名字 "


def _do_something():
    print("做秘密的事...")


# base15_1.base15_1.py:  base15_1.base15_1
print("base15_1.base15_1.py: ", __name__)
