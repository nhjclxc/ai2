#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:07
# Module    : activity.py
# explain   :
from fastapi import Query

import app.services.activity_service as activity_service
from app.schemas.activity import CreateActivityRequest
from app.models.activity import ActivityStatus

from typing import Annotated
from fastapi import APIRouter, Body
from .api import success,error


activity_router = APIRouter(
    prefix="/activity",
    tags=["activity"],
)

"""
{
    "name": "抽奖活动",
    "status": "draft",
    "start_time": "2026-04-23T10:00:00",
    "end_time": "2026-04-30T23:59:59",
    "rule_config": {
        "max_draw_times": 3,
        "probability": 0.2,
        "blacklist_users": ["user1", "user2"],
        "whitelist_users": ["user5", "user6"],
    }
}
"""
@activity_router.post("/create_activity")
async def create_activity(req_activity: Annotated[CreateActivityRequest, Body()]):
    return await activity_service.create_activity(req_activity)


@activity_router.get("/get_activity_by_id")
async def get_activity_by_id(activity_id: Annotated[int, Query()]):
    res = await activity_service.get_activity_by_id(activity_id)
    return success(res)

@activity_router.patch("/update_activity_status")
async def update_activity_status(
        activity_id: Annotated[int, Query()],
        status: Annotated[ActivityStatus, Query()]):
    res = await activity_service.update_activity_status(activity_id, status)
    return success(res)

@activity_router.get("/get_activity_status")
async def get_activity_status(activity_id: Annotated[int, Query()]):
    res = await activity_service.get_activity_status(activity_id)
    return success(res)


@activity_router.put("/draw")
async def draw(activity_id: Annotated[int, Query()],
                user_id: Annotated[int, Query()]):
    res = await activity_service.draw(activity_id, user_id)
    return success(res)