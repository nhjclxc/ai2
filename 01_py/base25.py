#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/24 18:43
# Module    : base25.py
# explain   : time模块，https://docs.python.org/zh-cn/3.10/library/time.html

# py时间的表示方式
# 1、自定义时间表示格式
# 2、时间元组
# 3、时间戳
# 4、py默认时间格式

import time

# 1、自定义时间格式
str_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(str_time)

# 2、返回时间元组
print(time.gmtime())

# 3、返回浮点型的时间戳
print(time.time())

# 4、返回py内置的时间格式
print(time.ctime())

# 1字符串时间 转 2时间元组：time.strptime
time_tp = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
print(time_tp)
print(time_tp.tm_year)
print(time_tp.tm_mon)

#  2时间元组 转 1字符串时间：time.strftime
time_s = time.strftime("%Y-%m-%d %H:%M:%S", time_tp)
print(time_s)

#  2时间元组 转 3时间戳：time.mktime
ts = time.mktime(time_tp)
print(ts)

#  3时间戳 转 2时间元组：time.gmtime
print(time.gmtime(ts))

#  2时间元组 转 4固定格式时间：time.mktime
f_time = time.asctime(time_tp)
print(f_time)

#  3时间戳 转 4固定格式时间：time.ctime
print(time.ctime(ts))

# 延时操作：time.sleep
# int(time.time())返回秒级时间戳
print("开始s：", int(time.time()))
print("开始ms：", int(time.time_ns() / (1000 * 1000)))
print("开始ns：", int(time.time_ns()))
time.sleep(1)
print("结束：", int(time.time()))

from datetime import datetime, timezone

# 秒
ts_sec = int(datetime.now(timezone.utc).timestamp())
print(ts_sec)

# 毫秒
ts_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
print(ts_ms)

print()
