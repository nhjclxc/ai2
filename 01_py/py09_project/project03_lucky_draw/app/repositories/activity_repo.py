#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:07
# Module    : activity_repo.py
# explain   :

from sqlalchemy import Column, Integer, String, update, select, Sequence, func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from watchfiles import awatch

from app.core.db_mysql import get_session, get_async_session_local
from app.models.activity import Activity, ActivityStatus

async def create_activity(activity: Activity) -> Activity:
    async with get_session(get_async_session_local()) as session:  # AsyncSession
        session.add(activity)
        await session.commit()
        session.refresh(activity)
        return activity


async def get_activity(activity_id: int) -> Activity:
    async with get_session(get_async_session_local()) as session:  # AsyncSession
        result = await session.execute(
            select(Activity).options(selectinload(Activity.prizes)).where(Activity.id == activity_id)
        )

        activity = result.scalar_one_or_none()
        return activity

async def update_activity_status(activity_id: int, status: ActivityStatus) -> bool:
    async with get_session(get_async_session_local()) as session:   # AsyncSession
        db_activity = await session.get(Activity, activity_id)
        if db_activity is None:
            return False
        db_activity.status = status
        # 自动提交事务之后，数据库即可发生修改
        # await session.commit()

    return True
