#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:05
# Module    : user.py
# explain   :


from sqlalchemy import Column, Integer, String, Boolean
from app.core.db_mysql import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=True)
    vip = Column(Boolean, nullable=False, default=False)
