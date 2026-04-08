#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/7 21:17
# Module    : f18_依赖项_类依赖项.py
# explain   : https://fastapi.org.cn/tutorial/dependencies/classes-as-dependencies/

from fastapi import FastAPI, Depends

from typing import Annotated

app = FastAPI()

@app.get("/f18/")
async def f18_(id: int):
    print("enter id: ", id)
    return {"id": id}

class Cat:
    def __init__(self, name: str):
        self.name = name

tom = Cat("Tom")


# Python 类也是可调用的。
# 以下是不使用 from pydantic import BaseModel 以实现py类可以作为 fastapi 接收参数的示例
class CommonQueryPrarms:
    def __init__(self, skip: int = 1, limit: int = 10, create_at: int = None):
        self.skip = skip
        self.limit = limit
        self.create_at = create_at

# 使用 Depends(CommonQueryPrarms) 来指明这个要作为查询参数
# FastAPI会调用该类CommonQueryParams。这将创建一个该类的“实例”，并将该实例作为参数传递commons给您的函数。
@app.get("/f18/query")
async def f18_query(common: Annotated[CommonQueryPrarms, Depends()]):
    print("enter common: ", common)
    print("enter common.skip: ", common.skip)
    print("enter common.limit: ", common.limit)
    print("enter common.create_at: ", common.create_at)
    return {"common": common}
# curl "http://127.0.0.1:8020/f18/query?skip=11&limit=111&create_at=123456789"

# Python 函数同样也是可调用的。
async def common_parameters(create_at: int | None = None, skip: int = 1, limit: int = 10):
    return {"create_at": create_at, "skip": skip, "limit": limit}

@app.get("/f18/query2")
async def f18_query(common: Annotated[dict, Depends(common_parameters)]):
    print("query2 common: ", common)
    print("query2 common.skip: ", common["skip"])
    print("query2 common.limit: ", common["limit"])
    print("query2 common.create_at: ", common["create_at"])
    return {"common": common}
# curl "http://127.0.0.1:8020/f18/query2?skip=11&limit=111&create_at=123456789"
