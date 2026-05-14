#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:03
# Module    : db_mysql_sync.py
# explain   : 初始化 mysql 数据库

# sql02_database_async_connect.py
# 建立数据库的异步连接，适于用 fastapi 使用


from contextlib import asynccontextmanager, contextmanager

import sqlalchemy
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.orm.session import Session

# 异步连接字符串
# 同步驱动使用：pymysql，异步驱动使用：aiomysql
DATABASE_URL = "mysql+pymysql://root:root123@localhost:3306/mysqldb?charset=utf8mb4"
# DATABASE_URL = "mysql+aiomysql://root:root123@localhost:3306/mysqldb?charset=utf8mb4"

# 创建 Engine
_engine = sqlalchemy.create_engine(
    DATABASE_URL,
    echo=True,      # 输出 SQL 调试信息
    pool_size=10,   # 连接池大小
    max_overflow=20 # 额外可创建的连接数
)

def get_engine():
    return _engine

# 异步 Session
# _async_session_local = sessionmaker(
#     bind=_engine,
#     class_=AsyncSession,        # 🔥 必须指定
#     expire_on_commit=False      # 🔥 强烈建议 False
# )
_session_local = sessionmaker(
    bind=_engine,
    class_=Session,        # 🔥 必须指定
    expire_on_commit=False      # 🔥 强烈建议 False
)

# def get_async_session_local():
#     return _async_session_local
def get_session_local():
    return _session_local


class Base(DeclarativeBase):
    pass



def init_db():
    print("init db")
    Base.metadata.create_all(_engine)
    print("init db success")

# @asynccontextmanager
# async def get_session(async_session):
#     """
#     get_session
#         支持自动管理事务
#
#     用法
#         async with get_session(get_async_session_local()) as session:  # type: AsyncSession
#
#     """
#     async with async_session() as session:  # type: AsyncSession
#         try:
#             yield session
#             await session.commit()
#         except Exception:
#             await session.rollback()
#             raise
# @asynccontextmanager

@contextmanager
def get_session(session_local):
    """
    get_session
        支持自动管理事务

    用法
        async with get_session(get_session_local()) as session:  # type: AsyncSession

    """

    with session_local() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise