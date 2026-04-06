#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/5 16:18
# Module    : f06_初识fastapi.py
# explain   :

# 第 1 步：导入 FastAPI
import fastapi
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    price: float

# 第 2 步：创建一个 FastAPI "实例"
app = fastapi.FastAPI()

# 第 3 步：创建一个路径操作
# 注意注意注意：每一个操作（get，post...）的括号内部的字符串就是这个操作的路径，其中的 ”/“ 会直接影响访问路径，要特别注意路径中 / 的写法
@app.get("/")
# 第 4 步：定义路径操作函数
async def root():
    # 执行业务
    # ...
    # 第 5 步：返回内容
    return {"message11": "Hello World  11123"}

# 第 6 步：运行部署它，执行: fastapi dev .\f06_初识fastapi.py
@app.get("/get")
def item():
    return {"msg": "Hello World  item"}

@app.post("/post")
def post_item(item: Item = None):
    return {"data": f"item: {item}", "msg": "post item"}

@app.put("/put")
def put_item(item: Item = None):
    return {"data": f"item: {item}", "msg": "put item"}

@app.delete("/delete")
def delete_item(id: int):
    return {"data": f"id: {id}", "msg": "delete item"}



