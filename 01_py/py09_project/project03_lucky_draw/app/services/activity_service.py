#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:06
# Module    : activity_service.py
# explain   :
import json
import random
from datetime import datetime
from typing import Any

from app.models.activity import Activity, ActivityStatus
from app.schemas.activity import CreateActivityRequest
import app.repositories.activity_repo as activity_repo
from app.exceptions.business_exception import BusinessException
from app.core.logger import logger

async def create_activity(req_activity: CreateActivityRequest) -> Activity:
    print(f"req_activity :  : {req_activity}")
    now = datetime.now()
    if  req_activity.start_time > req_activity.end_time:
        raise BusinessException(50010, "活动时间不合法！！！")
    if req_activity.start_time < now:
        raise BusinessException(50011, "活动时间不在范围内！！！")
    if len(req_activity.name) < 5:
        raise BusinessException(50012, f"活动名称不合法, 霍东阁名称过短 {len(req_activity.name)}")

    orm_activity = req_activity.to_orm()
    print(f"orm_activity : {orm_activity}")
    db_activity = await activity_repo.create_activity(orm_activity)
    print(f"db_activity : {db_activity}")
    return db_activity

async def get_activity_by_id(activity_id: int) -> Activity:
    logger.info(f"activity_id : {activity_id}")
    db_activity = await activity_repo.get_activity(activity_id)
    return db_activity

async def update_activity_status(activity_id: int, status: ActivityStatus) -> bool:
    print(f"activity_id : {activity_id}")
    print(f"status : {status}")
    db_activity = await activity_repo.get_activity(activity_id)
    if not db_activity:
        raise BusinessException(50013, "该活动不存在")
    if db_activity.status == ActivityStatus.ONLINE:
        raise BusinessException(50014, "该活动已上线，不支持修改")
    if db_activity.status == status:
        raise BusinessException(50015, "该活动已处于该状态，无须修改")

    now = datetime.now()
    return await activity_repo.update_activity_status(activity_id, status)

async def get_activity_status(activity_id: int) -> ActivityStatus:
    db_activity = await activity_repo.get_activity(activity_id)
    if not db_activity:
        raise BusinessException(50016, "该活动不存在")

    return db_activity.status

import threading

user_id_draw_times_dict: dict[int, int] = {}

async def draw(activity_id: int, user_id: int) -> dict[str, Any]:

    db_activity = await activity_repo.get_activity(activity_id)

    if not db_activity:
        raise BusinessException(50013, "该活动不存在")
    if db_activity.status != ActivityStatus.ONLINE:
        raise BusinessException(50014, "当前活动未上线，不支持抽奖")

    logger.info(f"activity_id : {activity_id}, user_id : {user_id}, rule_config: {db_activity.rule_config}")
    # rule_json = json.load(db_activity.rule_config)
    # db_activity.rule_config返回的已经是字典数据了可以直接用
    rule_dict = db_activity.rule_config
    """
    {"blacklist": [1, 2], "probability": 0.2, "max_draw_times": 3, "whitelist": [5, 6]}
    """
    blacklist = rule_dict['blacklist']
    if user_id in blacklist:
        raise BusinessException(50017, "该用户被禁止参与该活动")

    whitelist = rule_dict['whitelist']
    if user_id not in whitelist:
        raise BusinessException(50017, "该用户不属于该抽奖活动，请先添加")

    max_draw_times = rule_dict['max_draw_times']
    lock = threading.Lock()
    with lock:
        draw_times = user_id_draw_times_dict.get(user_id, 0)
        if draw_times >= max_draw_times:
            raise BusinessException(50018, f"用户[{user_id}] 超出活动[{activity_id}] 的抽奖次数上限")
        draw_times += 1
        user_id_draw_times_dict[user_id] = draw_times


    r = random.randint(1, 10)
    resp = {
        "random": r,
        "user_id": user_id,
        "draw_times": draw_times,
        "probability": rule_dict['probability'],
        "max_draw_times": max_draw_times,
    }

    return resp

