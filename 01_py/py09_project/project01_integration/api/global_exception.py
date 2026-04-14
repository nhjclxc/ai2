#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/14 21:37
# Module    : global_exception.py
# explain   : 全局异常处理

from fastapi import Request
from fastapi.responses import JSONResponse


def register_exception(app):

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=200,
            content={
                "code": -1,
                "message": str(exc),
                "data": None
            }
        )