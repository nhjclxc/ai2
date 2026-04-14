#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/13 21:50
# Module    : user_api.py
# explain   :
from fastapi import APIRouter
from service.user_service import *


user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@user_router.get("/")
async def get_user():
    print("get user")
    return {"hello": "world"}


