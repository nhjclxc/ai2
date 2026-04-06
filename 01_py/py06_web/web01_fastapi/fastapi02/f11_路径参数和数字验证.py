#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/6 11:18
# Module    : f11_路径参数和数字验证.py
# explain   : https://fastapi.org.cn/tutorial/path-params-numeric-validations/

from fastapi import FastAPI, Path, Query

# 要用验证的时候就要导入下面这个包
from typing import Annotated

app = FastAPI()

@app.get("/item/{item_id}")
async def get_item(item_id: Annotated[str, Path(max_length=5)]):
    return {"item_id": item_id}


# 数字验证
@app.get("/item")
async def item(id: Annotated[int, Query(gt=5, lt=10)]):
    return {"id": id}


