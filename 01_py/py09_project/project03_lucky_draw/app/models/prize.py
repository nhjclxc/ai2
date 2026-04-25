#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:04
# Module    : prize.py
# explain   : 活动奖品
from sqlalchemy.orm import relationship

from app.core.db_mysql import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Float


class Prize(Base):
    __tablename__ = "prize"
    # 主键id
    id = Column(Integer, primary_key=True)
    # 奖品名称
    name = Column(String(50), nullable=False)
    # 概率
    probability = Column(Float)
    # 库存
    stock = Column(Integer)

    # 奖品所属活动id activity.id
    activity_id = Column(Integer,  ForeignKey("activity.id"))

    # 与主表定义相呼应
    # Activity 主表的实体类
    # prizes 是主表中对应实体中定义子表实体的属性名
    # 数据库层面的关联靠上面的ForeignKey("activity.id")
    activity = relationship("Activity", back_populates="prizes")



    pass

