#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/14 21:47
# Module    : logging_middleware.py
# explain   : 请求日志中间件
import time
import json
from fastapi import Request


async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    # ===== 1. 获取请求体（重点坑点）=====
    body_bytes = await request.body()

    try:
        body = json.loads(body_bytes.decode()) if body_bytes else {}
    except Exception:
        body = body_bytes.decode(errors="ignore")

    # ===== 2. 获取 query 参数 =====
    query_params = dict(request.query_params)

    # ===== 3. 获取 path 参数 =====
    path_params = request.path_params

    # ===== 4. 打印日志 =====
    print("======== REQUEST LOG ========")
    print(f"method: {request.method}")
    print(f"url: {request.url}")
    print(f"path_params: {path_params}")
    print(f"query_params: {query_params}")
    print(f"body: {body}")

    # ⚠️ 重点：body 只能读一次，需要重建 request
    async def receive():
        return {"type": "http.request", "body": body_bytes}

    request._receive = receive

    # ===== 5. 执行请求 =====
    response = await call_next(request)

    # ===== 6. 响应时间 =====
    process_time = time.time() - start_time
    print(f"process_time: {process_time:.4f}s")
    print("======== END LOG ========\n")

    return response