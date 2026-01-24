#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/8 22:37
# Module    : base10.py
# explain   : 数据类型转化和


# 1、int()，将字符串转化为整数

num_str = "123"
print(num_str, type(num_str))
num_int = int(num_str)
print(num_int, type(num_int))

f = 3.14
print(f, type(f))
fi = int(f)
print(fi, type(fi))

print(int("+10"), int("-10"))

# 2、float()，将数据转化为浮点型
print(float(123))
print(float("123.456"))

# 3、str()，将数据转化为字符串类型

ss = str(10)
print(ss, type(ss))

#
li = [1, 2, 3]
lis = str(li)
print(lis, type(lis), type(lis[0]))

# list、dict、tuple，set
