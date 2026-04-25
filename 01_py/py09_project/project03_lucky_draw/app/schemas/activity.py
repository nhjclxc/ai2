#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:05
# Module    : activity.py
# explain   :
from datetime import datetime

from pydantic import BaseModel, Field
from typing import Dict, Any
from app.models.activity import ActivityStatus, Activity


class CreateActivityRequest(BaseModel):
    name: str | None = Field(default=None)
    status: ActivityStatus | None = Field(default=None)
    # "2000-05-23T10:00:00"
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)
    # 前端传json
    rule_config: Dict[str, Any] | None = None
    # rule_config: dict | None = None

    def to_orm(self) -> Activity:
        self_dict = self.model_dump()
        return Activity(**self_dict)

