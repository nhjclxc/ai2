#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/13 21:50
# Module    : user_repo.py
# explain   :
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from model.user import User
from pkg.db_msqyl import get_engine, get_session, get_async_session_local



async def select_user_by_id(user_id: int) -> User:
    async with get_session(get_async_session_local()) as session:  # type: AsyncSession
        # user: User | None  # Python 3.10+ 支持的写法
        # 最新等价写法：user: Optional[User]
        # 意思是：user 可能是一个 User 实例 或者 user 可能为 None
        user: Optional[User] = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return user


