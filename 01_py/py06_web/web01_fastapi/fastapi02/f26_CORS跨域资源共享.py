#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/8 20:25
# Module    : f26_CORS跨域资源共享.py
# explain   : https://fastapi.org.cn/tutorial/cors/

# 使用 CORSMiddleware 在您的 FastAPI 应用程序中进行配置。




from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}