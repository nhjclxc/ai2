#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/9 21:46
# Module    : base11.py
# explain   : 深浅拷贝，可变对象与不可变对象
import copy

# 浅拷贝，仅拷贝外层对象
# copy模块提供两个常用的方法，copy是浅拷贝方法，deepcopy是深拷贝方法
# 浅拷贝只会复制第一层的内容，深层的内容只会复制地址，不会创建新对象
# 深拷贝：外层数据和内层数据全部会重写创建一遍

# 浅拷贝
li1 = [1, 2, 3, 5, 6, [88, 99]]
li2 = copy.copy(li1)
print(id(li1), id(li1[5]), li1)
print(id(li2), id(li2[5]), li2)
li2.append(666)
li2[5].append(555)
print(id(li1), id(li1[5]), li1[5], li1)
print(id(li2), id(li2[5]), li2[5], li2)

# 2、深拷贝
li1 = [1, 2, 3, 5, 6, [88, 99]]
li2 = copy.deepcopy(li1)
print(id(li1), id(li1[5]), li1)
print(id(li2), id(li2[5]), li2)
li2.append(666)
li2[5].append(555)
print(id(li1), id(li1[5]), li1[5], li1)
print(id(li2), id(li2[5]), li2[5], li2)

# 3、可变对象：变量对应的值可以修改，但是内存地址不会发生改变
# 可变对象有：列表[1,2,3]、字典{1,2,3}、集合{"key":"value"}

# 4、不可变类型：存储空间保存的数据不允许被修改
# 不可变对象有：int、bool、float、complex、str、tuple

x1 = 666
print(x1, id(x1))
x1 = 999
print(x1, id(x1))
