#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/14 20:56
# Module    : api_response.py
# explain   :



from typing import Any, Optional
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: Optional[T] = None


class ResponseUtil:

    @staticmethod
    def success[T](data: Generic[T] = None):
        return ResponseModel(
            code=0,
            data=data
        )

    @staticmethod
    def error(message: str = "error", code: int = -1):
        return ResponseModel(
            code=code,
            message=message
        )