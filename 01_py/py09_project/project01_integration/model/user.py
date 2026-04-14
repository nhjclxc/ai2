#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/13 21:50
# Module    : user.py
# explain   :


from sqlalchemy import Column, Integer, String
from pkg.db_msqyl import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    # age = Column(Integer, nullable=False)


