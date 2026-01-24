#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/7 20:25
# Module    : base06.py
# explain   : py列表 https://docs.python.org/zh-cn/3.10/tutorial/introduction.html#lists

# 列表里面的元素数据类型可以不同


import copy

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print(lst[0])
print(lst[1])
print(lst[2])
print(lst[-1])
print(lst[-2])

for i in lst:
    print(i, end=" ")
print()

# 列表的切片操作
# lst[]

# 这是一个浅拷贝操作，[:]会创建一个长度和元素都一模一样的列表返回
# 当列表的数据类型是基础数据类型时，无所谓深拷贝/浅拷贝
# 而当列表的数据类型是引用数据类型的时候，那么就是浅拷贝操作了，[:]直接将元素的地址给新列表
lst2 = lst[:]
print(lst, lst2)
lst2[2] = 666
print(lst, lst2)

# 以下验证 [:] 的浅拷贝
arr1 = [1, 2, 3]
arr2 = [6, 7, 8]

arr22 = [arr1, arr2]
print(arr1, arr2, arr22)

arr22_tmp = arr22[:]
print(arr22, arr22_tmp)
# 修改arr22_tmp里面的一个元素，看看原数组arr22对应的元素是否被修改
arr22_tmp[0][0] = 666
# 以下输出：[[666, 2, 3], [6, 7, 8]] [[666, 2, 3], [6, 7, 8]]
# 表示我修改arr22_tmp的时候也修改到了arr22，所以[:]实际复制的是对象的地址，即执行浅拷贝操作
print(arr22, arr22_tmp)
# 注意：arr22.copy()也是浅拷贝

# 如何实现深拷贝？那么就要使用内置函数 copy.deepcopy()
arr22_tmp2 = copy.deepcopy(arr22)
print(arr22, arr22_tmp2)
arr22_tmp2[0][0] = 888
# 以下输出：[[666, 2, 3], [6, 7, 8]] [[888, 2, 3], [6, 7, 8]]
# 说明arr22_tmp2[0][0] = 888这一行操作没有修改到原数据
print(arr22, arr22_tmp2)

# 使用[]，置空列表
print(lst)
# 置空指定位置的元素
lst[2:6] = []
print(lst)
# 置空整个列表
lst = []
print(lst)

# 列表追加数据
lst.append(666)
lst.append(6 ** 2)
print(lst)

# 列表中range函数的使用
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for num in nums:
    print(num, end=("," if i < len(nums) - 1 else ""))
print()

# 使用range来遍历下标，这样就可以拥有元素的下标
for i in range(len(nums)):
    print(i, nums[i])
print()

# 使用 enumerate(iterable, start=0) 来包装列表，使其返回一个元组(index, value)
# 如果循环对象不是列表而是字典，那么可以使用字典自带的函数items()实现和enumerate方法同样的效果，但是字典返回的是(key,value)
for i, val in enumerate(nums):
    print(i, val)
    pass

"""
# 列表的相关操作， https://docs.python.org/zh-cn/3.10/tutorial/datastructures.html#more-on-lists

5.1. 列表详解¶
列表数据类型支持很多方法，列表对象的所有方法所示如下：

list.append(x)
在列表末尾添加一个元素，相当于 a[len(a):] = [x] 。

list.extend(iterable)
用可迭代对象的元素扩展列表。相当于 a[len(a):] = iterable 。

list.insert(i, x)
在指定位置插入元素。第一个参数是插入元素的索引，因此，a.insert(0, x) 在列表开头插入元素， a.insert(len(a), x) 等同于 a.append(x) 。

list.remove(x)
从列表中删除第一个值为 x 的元素。未找到指定元素时，触发 ValueError 异常。

list.pop([i])
删除列表中指定位置的元素，并返回被删除的元素。未指定位置时，a.pop() 删除并返回列表的最后一个元素。（方法签名中 i 两边的方括号表示该参数是可选的，不是要求输入方括号。这种表示法常见于 Python 参考库）。

list.clear()
删除列表里的所有元素，相当于 del a[:] 。

list.index(x[, start[, end]])
返回列表中第一个值为 x 的元素的零基索引。未找到指定元素时，触发 ValueError 异常。

可选参数 start 和 end 是切片符号，用于将搜索限制为列表的特定子序列。返回的索引是相对于整个序列的开始计算的，而不是 start 参数。

list.count(x)
返回列表中元素 x 出现的次数。

list.sort(*, key=None, reverse=False)
就地排序列表中的元素（要了解自定义排序参数，详见 sorted()）。

list.reverse()
翻转列表中的元素。

list.copy()
返回列表的浅拷贝。相当于 a[:] 。
"""

# 添加元素
# 使用一堆[]创建列表
color = ["red", "green", "blue"]
print(color)
color[len(color) - 1] = "black2"
print(color)
color.append("black")
print(color)
color.insert(0, "pink2")
print(color)
color[0] = "pink"
print(color)
# extend将一个列表解开然后追加
color.extend(["yellow", "pink", "white"])
print(color)

# 修改元素，直接通过下标进行修改
print(color[2])
color[2] = "asc sacas"
print(color[2])

# 查找元素：in，not in，index，count

print("green" in color)
print("green" not in color)
# ele = "green1"
ele = "green"
if ele in color:
    red_index = color.index(ele)
    print(f"element [{ele}] index is {red_index}")
else:
    print(f"element [{ele}] is not in color")

print(color.count(ele))
print(color.count("ele"))

# 删除元素：del，pop，remove
print("---------------删除元素------------------")
print(color)
# 表示删除某个位置的元素
del color[1]
print(color)
# 表示删除整个列表，就像整个列表从来没有被定义过一样
# del color
# print(color)  # NameError: name 'color' is not defined
# print(color222)  # NameError: name 'color222' is not defined

# remove(ele)从列表中删除第一个值为ele的元素
x = color.remove("pink")
print(x, color)
# x = color.remove("pink")
# print(x, color)
# ValueError: list.remove(x): x not in list
# x1 = color.remove("pink")
# print(x1, color)

last = color.pop()
print(last, color)

try:
    pink_index = color.index("pink")
    print(pink_index, color[pink_index])
except ValueError:
    print("未找到元素[pink]")
    pass

# 反转列表
print(color)
re_color = color.reverse()
# [...], None 可以得出 reverse() 是就地反转列表
print(color, re_color)

"""
#  列表推导式
格式1：[表达式 for 变量 in 可迭代对象]
格式2：[表达式 for 变量 in 可迭代对象 if 条件]
"""
li = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(li)
# 将每个元素*2返回到新列表里面
li2 = [item * 2 for item in li]
print(li2)

# 将所有的计数扩大两倍返回新的列表
lij3 = [item * 3 for item in li if item % 2 != 0]
print(lij3)

# 多级列表推导式
li33 = [(i, j) for i in [1, 2, 3] for j in [6, 7, 8]]
print(li33)
