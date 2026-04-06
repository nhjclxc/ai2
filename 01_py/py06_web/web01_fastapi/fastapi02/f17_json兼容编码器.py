#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/6 19:37
# Module    : f17_json兼容编码器.py
# explain   : https://fastapi.org.cn/tutorial/encoder/#using-the-jsonable-encoder
import datetime

from pydantic import BaseModel
from typing import Any
from fastapi.encoders import jsonable_encoder

class Item(BaseModel):
    name: str
    desc: str
    price: float
    now: datetime.datetime
    kwargs: dict[str, Any]

map = {
    "item": "Item",
    "a": 123,
    "b": 12311,
}
item = Item(name="item.name", desc="ResponseItem description", price=5.0, now=datetime.datetime.now(), kwargs=map)
print(item)
json_compatible_item_data = jsonable_encoder(item)
print(json_compatible_item_data)

print("-"*50)
print(item.model_dump_json())


print("-"*50)
import json
print(json.dumps(item.model_dump(), default=str))
