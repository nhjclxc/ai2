#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/5 11:38
# Module    : main.py
# explain   :
from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# 如果您的代码使用 async / await，请使用 async def
# 如果函数内部要使用异步，那么必须在接口函数上面加一个 async 关键字

# curl http://127.0.0.1:8000/items/5?q=somequery
@app.get("/items/async/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
# async def read_item(item_id: int, q: Optional[str] = None):
async def read_item(item_id: int, q: str | None = None):
    return {"item_id111212": item_id, "q": q}

@app.post("/items")
def create_item(item: Item):
    print(f"接收到的数据：{item.dict()}")
    return item

# uvicorn main:app --reload
# fastapi dev mian.py

# uv venv .venv

# Windows 激活uv虚拟环境：.venv\Scripts\activate.bat
#  Linux/macOS 激活uv虚拟环境：source .venv/bin/activate
# uv pip install -r requirements.txt