#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/5 14:45
# Module    : f02_sync.py
# explain   : 并发和 async / await
# explain   : https://fastapi.org.cn/async/
import fastapi

app = fastapi.FastAPI()

# 注意：如果在某个接口内部，要使用异步编程的话必须在 fastapi接口方法前面加一个 async 关键字

def some_library():
    # some_library 是一个将使用异步的函数
    pass
@app.get('/')
async def read_results():
    # await 就是异步等待结果
    results = await some_library()
    return results


# fastapi的接口函数上面是否添加async的区别？会不会影响性能，建议所有函数都添加吗？
import time

@app.get('/sync1')
def async1():
    start = time.time()
    time.sleep(2)
    now = time.time()
    return f"diff: {now - start}"

@app.get('/async1')
async def async1():
    start = time.time()
    time.sleep(2)
    now = time.time()
    return f"diff: {now - start}"

import asyncio
async def async2_func_func():
    # time.sleep(2)# 阻塞
    await asyncio.sleep(2)   # ✅ 非阻塞
    pass

async def async2_func():
    for i in range(3):
        await async2_func_func()

@app.get('/async2')
async def async2():
    start = time.time()
    await async2_func()
    now = time.time()
    return f"diff: {now - start}"

# C:\Users\nhjcl>curl http://localhost:8001/sync1
# "diff: 2.0141959190368652"
# C:\Users\nhjcl>curl http://localhost:8001/async1
# "diff: 2.009340286254883"
# C:\Users\nhjcl>curl http://localhost:8001/async2
# "diff: 2.002984046936035"



