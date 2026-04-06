#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/6 13:59
# Module    : f12_Header参数.py
# explain   : https://fastapi.org.cn/tutorial/header-params/

from fastapi import Depends, FastAPI, Header
from typing import Annotated

from pydantic import BaseModel

app = FastAPI()


# 使用与 Path、Query 和 Cookie 相同的结构来声明 Header 参数。
# 要声明 Header，你需要使用 Header，否则参数将被解释为查询参数。

# 默认情况下，Header 会将参数名称中的下划线 (_) 转换为连字符 (-)，以便提取和记录 Header。
# HTTP Header 是不区分大小写的，所以你可以使用标准的 Python 样式（也称为“snake_case”）来声明它们。

@app.get("/header")
async def header(
        user_agent: Annotated[str, Header()],
        token: Annotated[str, Header()],
):
    print("user_agent:", user_agent)
    print("token:", token)
    return {"user_agent": user_agent, "token": token}
# C:\Users\nhjcl>curl "http://127.0.0.1:8010/header" -H token:zxc123
# {"user_agent":"curl/8.18.0","token":"zxc123"}



# Header 参数模型, https://fastapi.org.cn/tutorial/header-param-models/
class HeaderItem2(BaseModel):
    user_agent: str
    token: str
    key: str

@app.get("/h2")
async def header2(headers : Annotated[HeaderItem2, Header()]):
    print("headers:", headers)
    return {"headers": headers}

# curl "http://127.0.0.1:8010/h2" -H token:zxc123 -H key:key-value -H key2:key-value



