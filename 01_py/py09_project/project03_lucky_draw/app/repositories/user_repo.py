#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:07
# Module    : user_repo.py
# explain   :
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.db_mysql import get_session, get_async_session_local

async def create_user(user: User) -> User:
    """
        保存用户
    :param user: 新增的用户数据
    :return: 返回包含数据库id的用户数据
    """
    async with get_session(get_async_session_local()) as session:  # type: AsyncSession
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user