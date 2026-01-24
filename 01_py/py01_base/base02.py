#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/6 21:16
# Module    : base02.py
# explain   : if表达式


age = 70

if 18 <= age < 60:
    print("你可以去上网了！！！")
elif age >= 60:
    print("去晒太阳吧")
else:
    print("你上个球的网")

# 三目运算
# 真执行的语句 if 条件表达式 else 为假执行的表达式

num = 18
print(num + 2 if num >= 18 else num - 2)

# 默认值操作
flag = num >= 18
print(flag)
flag = True if num >= 18 else False
print(flag)

# match语句，类似go的 switch 语句
# match 语句接受一个表达式并把它的值与一个或多个 case 块给出的一系列模式进行比较。
# py的match不需要使用break来推出，当匹配到一个的时候就会执行那个匹配到的块，执行完毕之后推出match语句
# 技巧：把match当作分类器，相同的操作在match语句之后一起执行，不要当道match里面

code = 503
match code:
    # 可以使用 | 来组合多个匹配结果
    case 200 | 201 | 202:
        print("执行成功")
    case 404:
        print("Not Of Found")
    case 500:
        print("Server Error")
    case _:
        # 这个 _ 匹配表示默认匹配，类似于 default
        print("未知的异常")

# 解构（序列模式）
point = (10, 0)
match point:
    case (0, 0):
        print("origin")
    case (x, 0):
        print(f"x axis, x={x}")
    case (0, y):
        print(f"y axis, y={y}")
    case (x, y):
        print(f"point ({x}, {y})")

# 带条件的匹配（守卫）
n = 55
match n:
    case x if x > 0:
        print("positive")
    case x if x < 0:
        print("negative")
    case 0:
        print("zero")

# 字典匹配
data = {"type": "login", "user": "tom"}

match data:
    case {"type": "login", "user": user}:
        print(f"{user} logged in")
    case {"type": "logout", "user": user}:
        print(f"{user} logged out")
