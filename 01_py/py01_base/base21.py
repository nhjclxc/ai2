#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/23 21:32
# Module    : base21.py
# explain   : 线程，https://docs.python.org/zh-cn/3.10/library/threading.html#module-threading
# 必须导入以下包
import threading

import time

# from threading import Thread

print(threading.current_thread().name)  # MainThread

print("------------------- 一、使用线程 ----------------------")


# 1、定义线程要执行的任务
# 创建一个函数用于子线程执行任务
def worker(name):
    time.sleep(1)
    print(f"{threading.current_thread().name} 正在worker执行 {name}")


# 2、创建子线程, target参数是目标函数，name是子线程名称，args是目标函数的参数
subT = threading.Thread(target=worker, name="subThread", args=("Tom",))
# 3、开启线程
subT.start()
# 4、等待子线程执行完毕, timeout=3指的是等待时长, 如果timeout不传表示必须等待子线程执行完毕
subT.join(timeout=3)
print("子线程执行完毕！！！")

print("------------------- 二、多线程并发执行 ----------------------")

print(f"开始: {int(time.time())}")


def worker2(*args):
    time.sleep(1)
    print(f"   {threading.current_thread().name} 正在执行任务 {args}")


threads = []
for i in range(5):
    t = threading.Thread(target=worker2, name=f"subThread{i}", args=(i,))
    t.start()
    # 注意：不得在此处执行t.join()方法，如果在这里执行t.join的话就和不开线程差不多了
    # 因为t.join会等待这次开启的线程执行完毕，之后再开下一个线程，导致所有线程都是顺序执行
    # t.join()
    # 要使用以下方法将所有子线程加入列表，将所有子线程都开启之后再去等待
    threads.append(t)

# 等待所有子线程执行完毕
for t in threads:
    t.join()

print(f"结束: {int(time.time())}")
print("多线程并发执行完毕")

print("------------------- 三、多线程并发数据竞争问题 ----------------------")

globalCount = 0


def autoIncr():
    global globalCount
    for i in range(1000):
        globalCount += 1


ts = [threading.Thread(target=autoIncr) for _ in range(50)]
for t in ts: t.start()
for t in ts: t.join()
# 正常情况下应该是：5000，可能是其他值，因为多线程存在竞争
print("执行完毕3: ", globalCount)
"""
线程 A 读到 globalCount = 100
线程 B 也读到 globalCount = 100
线程 A 写回 101
线程 B 写回 101   ← A 的结果被覆盖
"""
# 因此需要使用锁来防止多线程竞争资源
globalCount2 = 0
# 获取线程锁
lock = threading.Lock()


def autoIncr2():
    global globalCount2
    for _ in range(1000):
        with lock:
            globalCount2 += 1


# 批量创建
ts2 = [threading.Thread(target=autoIncr2) for _ in range(50)]
# 批量开启
for t in ts2: t.start()
# 批量等待
for t in ts2: t.join()
print("执行完毕-加锁: ", globalCount2)
