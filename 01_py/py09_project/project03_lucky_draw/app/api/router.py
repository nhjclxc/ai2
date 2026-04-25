#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:41
# Module    : router.py
# explain   :


from fastapi import APIRouter
from app.api.user_api import user_router
from app.api.activity_api import activity_router

api_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

api_router.include_router(user_router)
api_router.include_router(activity_router)
