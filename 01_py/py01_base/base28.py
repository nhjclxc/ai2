#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/24 19:15
# Module    : base28.py
# explain   : random模块，https://docs.python.org/zh-cn/3.10/library/random.html

import random
import time

random.seed(time.time_ns())

print(random.randint(0, 10))
print(random.randint(5, 10))
print(random.randrange(0, 10))

lst = [1, 2, 3, 5, 6, 8, 9]
# 从非空序列中随机返回数据， k表示返回几个数据
print(random.choices(lst, k=2))
# 将给定序列就地打乱，
random.shuffle(lst)
print(lst)

# 返回从总体序列或集合中选择的唯一元素的 k 长度列表。 用于无重复的随机抽样。
# 从给定序列中返回不重复的k个数据
print(random.sample(lst, 2))

# 在[a,b)返回内返回一个随机浮点数n
print(random.uniform(5, 10))
