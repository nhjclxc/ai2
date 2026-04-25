#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:04
# Module    : activity.py
# explain   : 活动
from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String, JSON, Enum, DateTime
from sqlalchemy.orm import Mapped, relationship

from app.core.db_mysql import Base
import enum

from app.models.prize import Prize


class ActivityStatus(enum.Enum):
    # 未发布
    DRAFT = "draft"
    # 活动正在进行
    ONLINE = "online"
    # 活动结束
    OFFLINE = "offline"

class Activity(Base):
    __tablename__ = "activity"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    # status(draft / online / offline), 如何给status定义枚举
    status = Column(Enum(ActivityStatus), nullable=False, default=ActivityStatus.DRAFT)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    # rule_config在数据库里面存储JSON
    rule_config = Column(JSON, nullable=False)


    # 主表和子表双向定义既可以实现主表向下访问子表的数据，也可以实现子表向上访问
    # 实现一对多（User ↔ Message）
    #
    # Mapped映射里面的字符串是类名，不是表名
    # relationship 是定义ORM对象之间的关系，不是数据库层面的关系
    # List["Prize"]表示返回的是数组，注意在ORM里面Prize这个是实体类名
    # activity是子表实体类中定义的主表实体类的属性名
    # 下面的是两个实体类的属性名到属性名之间的绑定
    prizes: Mapped[List["Prize"]] = relationship(back_populates="activity")
    # 如果不想在主表实体类和子表实体类进行双向绑定
    # prizes: Mapped[List["Prize"]] = relationship()

    def is_active(self):
        now = datetime.utcnow()
        return (
                self.status == ActivityStatus.ONLINE
                and (self.start_time <= now <= self.end_time)
        )
