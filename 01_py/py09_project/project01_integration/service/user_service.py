#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/13 21:50
# Module    : user_service.py
# explain   :
from fastapi import HTTPException

from model.user import User
import repo.user_repo as user_repo

async def get_user_by_id(user_id: int) -> User:
    if user_id is None:
        raise HTTPException(status_code=404, detail=f"user_id is required !!!")

    res = await user_repo.select_user_by_id(user_id)

    return res