#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/6 21:16
# Module    : base02.py
# explain   :  循环

# 1、while
# 2、for
# 3、break，continue的使用


# 1、while
"""

定义初始循环变量
while 循环条件:
    循环体
    改变循环变量

"""
# 注意：python不支持++和--操作
# 只能通过 i += 1或是 i-=1完成相应操作


num = 1
while num <= 10:
    print(num)
    num += 1

print()
while True:
    print(num)
    num -= 1
    if num <= 0:
        break

print()
while True:
    num += 1
    if num % 2 == 0:
        continue
    print(num)
    if num > 10:
        break

a = 1
while a:
    print("输出a: ", a)
    break
b = 2
while b:
    print("输出b: ", b)
    break

# 除False和0以外的其他数据，都是True
c = 0
while c:
    print("输出c: ", c)
    break

sum = 0
cursor = 0
while cursor <= 100:
    sum += cursor
    cursor += 1

print("1+2+3...+100 = ", sum)

i, j = 1, 1
while i <= 9:
    j = 1
    while j <= i:
        # 2表示输出的数据宽度
        # d表示输出的数据是数字类型
        print(f"{i} * {j} = {i * j:2d}", end=", " if j < i else "\n")
        j += 1
    i += 1

# 使用while实现斐波那契数列
a, b = 0, 1
i = 0
while i < 5:
    print(a)
    a, b = b, a + b
    i += 1

# 2、for
"""
for循环基本格式

for 临时变量 in 可迭代对象:
    循环体

"""

str = "Hello World!"
for c in str:
    print(c, end="-")

print()

#  range计数器
# range(start, stop, step),其中范围是[start, stop)，前闭后开
for i in range(10):
    print(i, end=" ")

print()
for i in range(5, 10):
    print(i, end=" ")

print()
for i in range(5, 10, 2):
    print(i, end=" ")
print()

sum2 = 0
for i in range(1, 101):
    sum2 += i
print(sum2)
