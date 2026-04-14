#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/13 21:50
# Module    : user_api.py
# explain   :
from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.params import Query

from api.api_response import ResponseUtil
from entity.user_enetity import RequestUser, UserResponse
import service.user_service as user_service
from middleware.token_middleware import LoginUserInfo, get_current_user
from model.user import User

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@user_router.post("/get_by_id")
async def get_user_by_id(req_user: Annotated[RequestUser, Body()]):
    print(f"len(req_user): {req_user}")
    orm_user = req_user.to_orm()
    res = await user_service.get_user_by_id(orm_user.id)
    return ResponseUtil.success(res)

# curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoyMTM2Mzc5ODYwfQ.hTQrBiY-Fuj0qVCxdvX1HrjGX8it5Gt7N80hMqeBFuY" http://127.0.0.1:6003/admin/user/get_by_id2?user_id=2

@user_router.get("/get_by_id2")
async def get_by_id2(current_user: Annotated[LoginUserInfo, Depends(get_current_user)]):
    print(f"current_user: {current_user}")
    res = await user_service.get_user_by_id(current_user.age)
    r = ResponseUtil.success(res)
    resp_user = UserResponse.model_validate(res)
    r2 =  ResponseUtil.success(resp_user)
    print(f"r: {r}")
    print(f"r2: {r2}")
    return r2
