#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/6 17:00
# Module    : f16_错误处理.py
# explain   : https://fastapi.org.cn/tutorial/handling-errors/

# 使用 HTTPException¶
# 要向客户端返回带有错误的 HTTP 响应，请使用 HTTPException。
# from fastapi import HTTPException


from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}

# curl "http://127.0.0.1:8082/items/foo"
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"Content-Type": "application/json", "X-Requesti-ID": item_id},
        )
    return {"item": items[item_id]}

# 添加全局异常处理程序
# 可以使用 [Starlette](https://www.starlette.dev/exceptions/) 的相同异常工具 添加自定义异常处理程序。

from fastapi import Request
from fastapi.responses import JSONResponse

# 一、自定义异常类
class IDNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        print(f"id不存在异常类：{self.message}")

# 二、添加 exception_handler 装饰器来处理全局异常，如果不添加 exception_handler 来处理全局异常，那么自定义异常将会被抛出，会影响服务
# 所有 @app.exception_handler 对应的处理函数必须要有两个参数，第一个是：当前请求 Request 对象；第二个是：当前异常抛出对象
@app.exception_handler(IDNotFoundException)
async def id_not_found(request: Request, exception: IDNotFoundException):
    return JSONResponse(status_code=404, content={"message": exception.message})

ids = (1,22,33)
@app.get("/exp")
async def exp(id: int):
    if id not in ids:
        raise IDNotFoundException(f"id={id} no in ids: {ids}")
    return {"data": id}

#  fastapi 有一个自己的全局异常处理程序，要覆盖它，请导入 StarletteHTTPException，
#  并使用 @app.exception_handler(StarletteHTTPException) 来装饰异常处理程序。
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print("enter http_exception_handler")
    return JSONResponse(status_code=exc.status_code, content={"message": "覆盖全局异常处理"})

@app.get("/exp2")
async def exp2(id: int):
    print("id", id)
    if id not in ids:
        print("找不到对应id")
        raise HTTPException(418)
    return {"data": id}



