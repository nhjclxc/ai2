#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/8 21:35
# Module    : base09.py
# explain   : 集合与字典，https://docs.python.org/zh-cn/3.10/tutorial/datastructures.html#sets
# 集合和字典都是使用一对大括号{}来创建的，
# 集合是直接将元素安顺序写进去：{1,2,3,4,5,6}
# 字典必须是k-v格式组合而成：{"k1":1,"k2":2,"k3":3}

s = {1, 2, 3, 4, 5, 6}
d = {"k1": 1, "k2": 2, "k3": 3}
print(s)
print(d)

print(" ------------------------ 集合 -------------------------------")
# 集合无序且不可重复
# 集合元素不可重复
s2 = {1, 2, 3, 4, 5, 6}
print(len(s2), s2)
# 5这个元素已经存在集合s2里面了，所以这个元素添加不进去
# 从而可得集合数据结构是不支持重复元素的，可用于元素去重的操作
s2.add(5)
print(len(s2), s2)
s2.add(8)
print(len(s2), s2)

# 将一个列表的元素去重
li = [1, 2, 3, 4, 5, 6, 2, 3, 2, 6, 5, 8, 9, 8, 6]
print(len(li), li)
lis = set()
for i in li:
    # 单个元素进行添加
    lis.add(i)
print(len(lis), lis)

li_set = set(li)
print(len(li_set), li_set)
# 批量元素进行添加
li_set.update([1, 2])
print(len(li_set), li_set)
li_set.update([11, 22])
print(len(li_set), li_set)

# 不能直接修改元素的值
# TypeError: 'set' object does not support item assignment
# li_set[1] = 666

# 删除元素的值
x = li_set.remove(4)
print(x, li_set)
# 如果remove的值不存在，将报错 KeyError: 4
# li_set.remove(4)
# 这时就要使用另一个方法discard
li_set.discard(4)
print(x, li_set)
li_set.discard(3)
print(x, li_set)
# pop将删除第一个元素
xx = li_set.pop()
print(xx, li_set)

print("-------------- 集合操作 --------------------")
s1 = {1, 2, 3, 4, 5, 6, 7}
s2 = {5, 6, 7, 8, 9, 0}
s3 = {1, 2, 3}
# 集合取交集
print(s1.intersection(s2))
print(s1 & s2)
# 取并集合
print(s1.union(s2))
print(s1 | s2)
# 取差集： s1中有，而s2中没有的元素
print(s1.difference(s2))
print(s1 - s2)
# 将两个集合的对称差返回为一个新的集合。（即所有恰好属于某一集合的元素。
print(s1.symmetric_difference(s2))
print(s1.difference(s2).union(s2.difference(s1)))

# s3是不是s1的子集
print(s3.issubset(s1))
print(s3.issubset(s2))

# 定义空集合
s1 = set()
print(s1, type(s1))

# 定义空字典
dic1 = {}
print(dic1, type(dic1))

print(" ------------------------ 字典 -------------------------------")

dic = {"name": "zhangsan", "age": 18}
print(dic, type(dic))
print(dic["name"])
print(dic["age"])
print(dic.keys())
z = dic.keys()
for i in z:
    print(i)

# 字典的增删改查
# 查看元素,
# 注意：字典中没有下标索引，只能使用字典的key来获取数据
print(dic["name"])
# 当使用[]读取的键不存在时会报错：KeyError: 'sex'
# print(dic["sex"])
# 要想不报错，那么就要使用dict提供的方法get来获取
print(dic.get("sex"))

# 修改元素
dic["age"] = 20
print(dic)
dic["sex"] = "男"
print(dic)

# 删除字典
del dic["age"]
print(dic)
# 删除不存在的键，KeyError: 'tel'
# del dic["tel"]

# 使用pop移除指定键，并且返回该键对应的数据
name_value = dic.pop("name")
print(name_value)
print(dic)

# 删除最后一个键值对
dic.popitem()

# del dic
# NameError: name 'dic' is not defined. Did you mean: 'dir'?
# print(dic)

# 清空所有的字典数据，但是对象开辟的空间还保留着，可以接着进行读写操作
dic.clear()
print(dic)
dic["addr"] = "北京市"
print(dic)
dic["name"] = "zhangsan"
dic["age"] = 18

# 字典的常见操作
print("字典长度：", len(dic))
print("获取字典的所有键集合：", dic.keys())
print("获取字典的所有值集合：", dic.values())
# 每一个键值对都是一个元组
print("返回字典里面所有的键值对，", dic.items())

# 字典的遍历
for k, v in dic.items():
    print(k, v)
for tp in dic.items():
    print(tp, tp[0], tp[1])

print()
# 如果直接遍历dic的话只能拿到一个key，不能拿到value
# ValueError: too many values to unpack (expected 2)
# for k, v in dic:
#     print("遍历方式2：", k, v)

# 虽然不能直接拿到key对应的value，但是可以通过key来获取对应的value
for key in dic:
    print("遍历方式2：", key, dic.get(key))

# 字典的应用场景
# 1、使用键值对存储描述物品的相关信息
