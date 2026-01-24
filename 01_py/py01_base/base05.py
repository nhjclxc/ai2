#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/7 20:25
# Module    : base05.py
# explain   : py字符串 https://docs.python.org/zh-cn/3.10/tutorial/introduction.html#strings

# 1、字符串的编码与解码
# str.encode，对str进行编码，可以通过encoding参数指定编码方式
# en_str.decode，对en_str进行解码（注意：en_str是被编码过后的字符串）

cstr = "hello world 你是？"
print(cstr, type(cstr))
print(cstr[0], cstr[1], cstr[2], )
print(cstr[-1], cstr[-2], cstr[-3], )

en_str = cstr.encode(encoding="utf-8")
print(en_str, type(en_str))
print(en_str[0], en_str[1], en_str[2], )

de_str = en_str.decode()
print(de_str, type(de_str))

# 2、字符串的常见操作

str1 = "你好啊"
str2 = "欢迎来到编程的世界"

# 字符串的连接操作 ”+“
cstr = str1 + "," + str2
print(cstr, type(cstr))
print(10 + 10)
print("10" + "10")
# TypeError: can only concatenate str (not "int") to str
# print("你好" + 10086)
# 要想将字符串和其他类型的数据进行拼接，必须使用字符串的格式化方法，如：format、f格式化等方法
num = 10086
print("你好{}".format(num))
print(f"你好{num}")

# 重复输出字符串
str3 = cstr * 2
print(str3)

# 通过索引获取字符串中的字符
print(cstr[0], cstr[1], cstr[2])

# 字符串的切片操作，截取部分字符串 [start:end:step]
print(cstr[:])
print(cstr[2:])
print(cstr[:8])
print(cstr[2:8])
print(cstr[2:8:2])
print(cstr[2:8:3])

# 判断是否包含子字符串
# 字符串的包含成员运算符， char in strings，包含返回True
print("好" in cstr)
print("你好" in cstr)
print("我" in cstr)
# 字符串的不包含成员运算符， char not in strings，不包含返回False
print("好" not in cstr)
print("你好" not in cstr)
print("我" not in cstr)

# 取字符串长度
print(len(cstr))

# 字符串的常见函数操作
# 完整字符串操作方法在：https://docs.python.org/zh-cn/3.10/library/stdtypes.html#string-methods
# find，count，replace，split
print(cstr.find("来到"))  # 返回子串的开始索引位置
print(cstr.find("来到", 7, 9))  # 没有找到返回-1

# count返回子串出现的重复次数
astr = "aabbccbbddbbeebbrrbb"
print(astr.count("b"))
print(astr.count("bb"))

# endswith判断是否是以这个子串结尾
# startwith判断是否是以这个子串开始
print(cstr.startswith("你好"))
print(cstr.startswith("你好2"))
print(cstr.endswith("世界"))
print(cstr.endswith("世界2"))

# index，返回子串的索引，功能类似find，但是index在没有找到子串的时候会发生ValueError
print(cstr.index("来到"))  # 返回子串的开始索引位置
# print(cstr.index("来到", 7, 9))  # 没有找到返回-1, ValueError: substring not found

# s.join(iterable)，返回一个由 iterable 中的字符串拼接而成的字符串。
# 即用s去连接iterable中的各个元素
lst = ["aa", "bb", "cc"]
join_str = ",".join(lst)
print(join_str)  # aa,bb,cc

# replace，字符串替换
print(cstr.replace("哦哦", "啊啊"))
print(cstr.replace("好", "GOOD"))

# slipt，对字符串进行切割
lst2 = join_str.split(",")
print(lst2, len(lst2))
