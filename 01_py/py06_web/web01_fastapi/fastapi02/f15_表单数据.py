#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/6 16:15
# Module    : f15_表单数据.py
# explain   : https://fastapi.org.cn/tutorial/request-forms/

# 要使用表单，请先安装 python-multipart。使用命令：pip install python-multipart


from fastapi import FastAPI, Form
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

@app.post("/form")
async def form(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    print("form:", username, password)
    return {"username": username, "password": password}


# 使用表单模型来接收参数
class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(user: Annotated[UserLogin, Form()]):
    print("login:", user)
    return {"username": user.username, "password": user.password}




# 要接收上传的文件，请先安装 python-multipart。使用命令：pip install python-multipart
from fastapi import File, UploadFile

# ❗ bytes → 一次性读入内存（适合小文件）
# ❗ UploadFile → 流式处理（适合大文件，推荐）

@app.post("/upload")
async def upload(file: Annotated[bytes, File()]):
    print("upload:", len(file))
    return {"filename": len(file)}

@app.post("/uploadFile")
async def upload_file(file: Annotated[UploadFile, File()]):
    print("upload_file:", file)

    return {"filename": file.filename}

# 表单 和 文件 同时使用
@app.post("/userUploadFile")
async def userUploadFile(username: Annotated[str, Form()], file: Annotated[UploadFile, File()]):
    print(f"username: {username}, file: {file.filename}")
    return {"filename": file.filename}