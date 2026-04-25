#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/23 21:06
# Module    : __init__.py
# explain   :
from . import user, activity, prize, user_draw_record

from .user import User
from .activity import Activity
# from .prize import Prize
# from .user_draw_record import UserDrawRecord


__all__ = [
    # 模块
    "user",
    "activity",
    # 类
    "User",
    "Activity",
]