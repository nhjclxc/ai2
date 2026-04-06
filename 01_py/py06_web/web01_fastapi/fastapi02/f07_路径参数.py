#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/5 16:54
# Module    : f07_路径参数.py
# explain   : f07_路径参数.py
# explain   : https://fastapi.org.cn/tutorial/path-params/

import fastapi

# 创建一个参数枚举类
from enum import Enum

class ItemType(str, Enum):
    type1 = "type1"
    type2 = "type2"
    type3 = "type3"

app = fastapi.FastAPI()

# 路径参数
# 如果不指定类型，那么可以默认接收了str 类型
@app.get("/item/{item_id}")
async def item(item_id: int):
    return {"item_id": f"item_id: {item_id}"}

@app.get("/itemarg/{item_arg}")
async def item(item_arg: int | str):
    return {"item_id": f"item_arg: {item_arg}"}


# curl http://127.0.0.1:8001/itemtype/type1
@app.get("/itemtype/{item_type}")
async def item(item_type: ItemType):
    print(f"item_type: {item_type}, item_type.value: {item_type.value}")
    receive_type = "接收到的类型："
    ret_enum=None
    if item_type is ItemType.type1:
        receive_type = receive_type + "type1"
        ret_enum=ItemType.type1
    elif item_type is ItemType.type2:
        receive_type = receive_type + "type2"
        ret_enum=ItemType.type2
    elif item_type == ItemType.type3:
        receive_type = receive_type + "type3"
        ret_enum=ItemType.type3
    else:
        receive_type = receive_type + "未知的类型，不予处理。"
    return {"receive_type": receive_type, "item_enum": ret_enum}


# 包含路径的路径参数
@app.get("/pathargs/{uri}")
async def path(uri: str):
    return {"uri": uri}
# C:\Users\nhjcl>curl http://127.0.0.1:8001/pathargs/test/static/js/index.js
# {"detail":"Not Found"}

# 包含路径的路径参数，要想获取后面的路径，必须在路径参数后面加一个:path
# 你需要告诉 FastAPI：👉 这个参数是“包含斜杠的路径”
# 即使用fastapi的 “路径转换器”， :path 告诉它该参数应匹配任何*路径*
@app.get("/pathargs2/{uri:path}")
async def path(uri: str):
    return {"uri": uri}
# C:\Users\nhjcl>curl http://127.0.0.1:8001/pathargs2/test/static/js/index.js
# {"uri":"test/static/js/index.js"}

