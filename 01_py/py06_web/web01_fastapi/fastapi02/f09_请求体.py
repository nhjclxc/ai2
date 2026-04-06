#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/5 17:59
# Module    : f09_请求体.py
# explain   : https://fastapi.org.cn/tutorial/body/

import fastapi
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = fastapi.FastAPI()


@app.post("/create")
async def create(item: Item):
    print(f"item: {item}")
    return {"item": item}

# get 操作也能使用类来接收参数, 但是必须修改一下接收参数的方法
from fastapi import Depends, Body

from typing import Annotated


@app.get("/get")
async def get(item: Item = Depends()):
    print(f"item: {item}")
    return {"item": item}

# C:\Users\nhjcl>curl "http://127.0.0.1:8001/get?description=description11&name=name121&price=123.25"
# {"item":{"name":"name121","description":"description11","price":123.25,"tax":null}}

# 同时声明请求体和路径参数
# FastAPI 将识别出与路径参数匹配的函数参数将*从路径中获取*，而声明为 Pydantic 模型 的函数参数将*从请求体中获取*。
@app.post("/create2")
async def create2(item: Item, age: int = 18):
    print(f"item: {item}, age: {age}")
    return {"item": item}

# 请求体 + 路径参数 + 查询参数
@app.post("/create3/{item_id}")
async def create3(item: Item, age: int = 18, item_id: int = -1):
    print(f"item: {item}, age: {age}, item_id: {item_id}")
    return {"item": item, "age": age, "item_id": item_id}
# 函数参数将识别如下：
# 如果参数也声明在路径中，则将其用作路径参数。
# 如果参数是单一类型（如 int、float、str、bool 等），则将其解释为查询参数。
# 如果参数被声明为Pydantic 模型的类型，则将其解释为请求体。




# 声明多个body参数

class User(BaseModel):
    user_id: str
    name: str
class Order(BaseModel):
    user_id: str
    order_id: str
    order_name: str

# FastAPI 会注意到函数中有多个 body 参数（有两个参数是 Pydantic 模型）。
# 因此，它将使用参数名称作为 body 中的键（字段名称），并期望一个 body，例如
"""
{
    "order": {
        "user_id": "user_id123",
        "order_id": "order_id789",
        "order_name": "Foo"
    },
    "user": {
        "user_id": "user_id123",
        "name": "Dave Grohl"
    }
}
"""
@app.post("/order")
async def order(user: User, order: Order):
    print(f"user: {user}")
    print(f"order: {order}")
    return {"user": user, "order": order}


# 如果只有一个body参数，那么fastapi就会直接将这个参数的json传入
"""
{
    "user_id": "user_id123",
    "order_id": "order_id789",
    "order_name": "Foo"
}
"""
@app.post("/order2")
async def order2(order: Order):
    print(f"order: {order}")
    return {"order": order}

# 但是有时候希望不要直接传入body，因为这个接口以后可能会扩展，因此我们希望声明一个body参数的时候也加一个orde的key来指明具体的json数据
# 使用以下方法
"""
{
    "order": {
        "user_id": "user_id123",
        "order_id": "order_id789",
        "order_name": "Foo"
    }
}
"""
@app.post("/order3")
async def order3(order: Annotated[Order, Body(embed=True)]):
    print(f"order: {order}")
    return {"order": order}



# 与您可以使用 Query、Path 和 Body 为路由函数参数声明额外的验证和元数据的方式相同，您也可以使用 Pydantic 的 Field 在 Pydantic 模型内部声明验证和元数据。
from pydantic import Field

class Task(BaseModel):
    user_id: int = Field(666, gt=1, lt=21)
    task_id: int
    task_name: str = Field("默认任务", max_length=5)

@app.post("/task")
async def task(task: Annotated[Task, Body(embed=True)]):
    print(f"task: {task}")
    return {"task": task}


# Body - 嵌套模型
class Address(BaseModel):
    city: str = Field("北京", max_length=5, min_length=2)
    street: str

class Score(BaseModel):
    score: float
    subject: str

from typing import Any
class Student(BaseModel):
    stu_id: int = Field(666, gt=1000, lt=9999)
    stu_name: str
    addr: Address
    # 声明带类型参数的 list¶
    # 要声明具有类型参数（内部类型）的类型，如 list、dict、tuple，请使用方括号：[ 和 ] 将内部类型作为“类型参数”传递。
    score: list[Score] = []
    tags: set[str] = []
    kwargs: dict[str, Any] = {}

"""
{
    "stu_id": 1001,
    "stu_name": "zhangsam",
    "addr": {
        "city": "上海",
        "street": "未知名街区"
    },
    "score": [
        {
            "score": 99.5,
            "subject": "数学"
        }
    ],
    "tags": ["a", "b", "c", "a", "b"],
    "kwargs": {
        "a1": "v1",
        "a2": "v2",
        "a3": "v3"
    }
}
"""
@app.post("/stu")
async def stu(student: Student):
    print(f"stu: {student}")
    return {"stu": student}

# 定义一个纯列表的请求
@app.post("/clist")
async def clist(ids: list[int]):
    print(f"ids: {ids}")
    return ids