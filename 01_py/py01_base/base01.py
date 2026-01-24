#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/6 20:57
# Module    : base01.py
# explain   :

num = 1
print(num)
print(type(1))
print(type(1.2))
print(type(-1.2))
print(type(-1.21234567))

print(type(True))
print(type(False))
print(True + False)
print(True + 1)
print(type(True + False))

# print(type(1+5i))  # SyntaxError: invalid decimal literal
print(type(1 + 5j))  # 虚部只能是j，不能变为其他的

a = 1 + 5j
b = 2 + 3j

print(a)
print(b)
print(a + b)

# 格式化方法

name = "zhangsan"
age = 18
# 1、%格式化
print("百分号格式化。名字：%s, 年龄：%d。" % (name, age))
print("format格式化。名字：{}, 年龄：{}。".format(name, age))
print("format格式化指定参数顺序。名字：{0}, 年龄：{1}。".format(name, age))
print("format格式化指定参数名称。名字：{n}, 年龄：{a}。".format(a=age, n=name))
print(f"f格式化。名字：{name}, 年龄：{age}。")
print(f"f格式化。名字：{name}, 年龄：{age:5d}。")
