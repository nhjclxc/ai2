#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/13 21:50
# Module    : msqyl_db.py
# explain   :


from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "mysql+aiomysql://root:root123@localhost:3306/mysqldb?charset=utf8mb4"

# 创建异步 Engine
_engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)

def get_engine():
    return _engine

# 异步 Session
_async_session_local = sessionmaker(
    bind=_engine,
    class_=AsyncSession,        # 🔥 必须指定
    expire_on_commit=False      # 🔥 强烈建议 False
)

def get_async_session_local():
    return _async_session_local


class Base(DeclarativeBase):
    pass


async def init_db():
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("init db success")


@asynccontextmanager
async def get_session(async_session):
    """
    get_session
        支持自动管理事务
    """
    async with async_session() as session:  # type: AsyncSession
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

