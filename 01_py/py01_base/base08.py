#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/8 21:20
# Module    : base08.py
# explain   : 元组，https://docs.python.org/zh-cn/3.10/tutorial/datastructures.html#tuples-and-sequences

# 注意，元组使用一堆括号()来定义，而列表则使用一堆中括号[]来定义
# 元组式不可修改对象，只支持读操作
# 列表是可修改对象，能支持增删改查

# 元组的应用场景：
# 1、作为函数的参数和返回值
# 2、%格式化输出的参数实质时元组
# 3、数据不允许被修改时，使用元组

tp = ("red", "greed", "pink", "red", "black", "blue")
print(tp[2])
print(tp.count("red"))
print(tp.index("pink"))
# ValueError: tuple.index(x): x not in tuple
# print(tp.index("pin222k"))


tp2 = (1, 2, 3, 5, 6, tp, [1, 2, 3])
print(tp2)
print(tp2[2])
print(tp2[5])
print(tp2[:3])

# 演示元组不能被修改
# TypeError: 'tuple' object does not support item assignment
# tp2[2] = 666  # 元组不支持项目赋值

# 元组打包与解包
x, y, z = 11, 22, 33
print(x, y, z)
xyz = (x, y, z,)
print(xyz)
x1, y1, z1 = xyz
print(x1, y1, z1)

# 定义一个元素的元组时，那一个元素后面必须加一个逗号,
t1 = (111)
t2 = (222,)
t3 = ()
print(t1, type(t1))
print(t2, type(t2))
print(t3, type(t3))
