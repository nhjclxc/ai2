#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/25 15:19
# Module    : api.py
# explain   : 包装全局响应结构

def success(data=None, msg="success"):
    return {
        "code": 200,
        "msg": msg,
        "data": data
    }

def error(code, msg):
    return {
        "code": code,
        "msg": msg,
        "data": None
    }