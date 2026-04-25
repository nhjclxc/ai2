#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:06
# Module    : user_service.py
# explain   :

from app.models.user import User
from app.schemas.user import CreateUserRequest
import app.repositories.user_repo as user_repo
from app.config.constants import user_age_required_over_18, user_name_len_required_over_6

async def create_user(c_user: CreateUserRequest) -> User:
    if c_user.age and c_user.age < 18:
        raise user_age_required_over_18

    if c_user.name and len(c_user.name) < 6:
        raise user_name_len_required_over_6

    user = await user_repo.create_user(c_user.to_orm())

    print(f"user_repo.create_user 成功：{user}")

    return user
