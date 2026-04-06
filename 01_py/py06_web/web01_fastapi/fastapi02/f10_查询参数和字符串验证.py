#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/6 10:43
# Module    : f10_查询参数和字符串验证.py
# explain   : https://fastapi.org.cn/tutorial/query-params-str-validations/

from fastapi import FastAPI

# 以下两个包实现字符串验证
from typing import Annotated
from fastapi import Query
# 除了query还有Path()、Body()、Header() 和 Cookie() 等，与 QUery的使用方法相同
# 注意：Query()、Path()、Body()、Header() 和 Cookie() 等必须搭配 Annotated 来使用
# 因为，Annotated 会把数据类型和数据验证做一层包装，而Query()等只是做一个数据验证，如果只写3Query这样的函数，那么就没有数据类型声明了
# Query()、Path()、Body()、Header() 和 Cookie() 等是“参数元信息（metadata）”，不是类型

app = FastAPI()

# FastAPI 允许您为参数声明额外的信息和验证。


# 要求对字符串 name 进行长度验证，要求不超过10个字符
@app.get("/get")
# async def get(name: str):
# Annotated 的第一个参数写数据类型，第二个参数写条件
# 使用 Query 来构建查询条件
# Annotated[str, Query(max_length=10)] 这个整体被单当作 name 的一个类型
async def get(name: Annotated[str, Query(max_length=10)]):
    print(f"get {name}, len={len(name)}")
    return {"name": name}

#           default_factory: () -> Any | None = _Unset,
#           alias: str | None = None,
#           alias_priority: int | None = _Unset,
#           validation_alias: str | AliasPath | AliasChoices | None = None,
#           serialization_alias: str | None = None,
#           title: str | None = None,
#           description: str | None = None,
#           gt: float | None = None,
#           ge: float | None = None,
#           lt: float | None = None,
#           le: float | None = None,
#           min_length: int | None = None,
#           max_length: int | None = None,
#           pattern: str | None = None,
#           regex: str | None = None,
#           discriminator: str | None = None,
#           strict: bool | None = _Unset,
#           multiple_of: float | None = _Unset,
#           allow_inf_nan: bool | None = _Unset,
#           max_digits: int | None = _Unset,
#           decimal_places: int | None = _Unset,
#           examples: list | None = None,
#           example: Any | None = _Unset,
#           openapi_examples: dict[str, Example] | None = None,
#           deprecated: deprecated | str | bool | None = None,
#           include_in_schema: bool = True,
#           json_schema_extra: dict[str, Any] | None = None,

@app.get("/get2")
async def get2(name: str | None):
    print(f"post {name}, len={len(name)}")
    return {"name": name}
@app.get("/get3")
async def get3(name: str = None):
    print(f"post {name}, len={len(name)}")
    return {"name": name}


# 接收别名参数
# curl "http://127.0.0.1:8003/get5?test-name=zxc213"
@app.get("/get5")
async def get5(test_name: Annotated[str, Query(alias="test-name")]):
    print(f"get {test_name}, len={len(test_name)}")
    return {"test_name": test_name}

# 弃用某个参数，将 deprecated=True 参数传递给 Query

from pydantic import BaseModel
from typing import Annotated

class FilterParams(BaseModel):
    limit: int = 1
    offset: int = 10
    create_at: int

# 查询参数模型
@app.get("/items")
async def item(filter_params: Annotated[FilterParams, Query()]):
    return {"param": filter_params}

# curl "http://127.0.0.1:8005/items?limit=2&offset=15&create_at=123456789"