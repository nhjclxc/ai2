#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:07
# Module    : user_api.py
# explain   :
from typing import Annotated
from fastapi import APIRouter, Body, Depends
from app.schemas.user import CreateUserRequest

import app.services.user_service as user_service

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@user_router.post("/create_user")
async def create_user(r_user: Annotated[CreateUserRequest, Body()]):
    return await user_service.create_user(r_user)


