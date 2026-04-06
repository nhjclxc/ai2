#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/6 15:47
# Module    : f13_响应模型.py
# explain   : https://fastapi.org.cn/tutorial/response-model/



from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Annotated, Any
from fastapi.responses import RedirectResponse
from pydantic.v1 import NoneStr

app = FastAPI()


class Item(BaseModel):
    name: str

class ResponseItem(BaseModel):
    name: str
    desc: str

# 定义函数的数据类型 -> Item: 就是定义fastapi操作的响应模型
# 同时可以在操作方法中添加response_model 为 ResponseItem，这样/docs就能解析这个响应的类型
@app.get("/item", response_model=ResponseItem)
async def item(item: Annotated[Item, Query()]) -> ResponseItem:
    print(f"item: {item}")
    resp_item = ResponseItem(name=item.name, desc="ResponseItem description")
    print(f"resp_item: {resp_item}")
    return resp_item

# 禁止将 输入模型作为输出模型返回， 特别是输入模型中有敏感数据的时候

class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: str
    full_name: str | None = None


@app.post("/user", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    print(f"user: {user}")
    # 使用 Pydantic 后 FastAPI 将负责过滤掉所有未在输出模型中声明的数据（）。
    return user

# http://127.0.0.1:8013/youtube
# Redirect to YouTube "No Time For Caution" By Interstellar
@app.get("/youtube")
async def get_youtube() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=2o9KfyPqQzY")

@app.get("/resp", response_model=None)
async def resp() -> ResponseItem:
    return ResponseItem(name="item.name", desc="ResponseItem description")
# 使用了response_model=None之后为什么还是可以得到响应数据
# C:\Users\nhjcl>curl http://127.0.0.1:8013/resp
# {"name":"item.name","desc":"ResponseItem description"}
