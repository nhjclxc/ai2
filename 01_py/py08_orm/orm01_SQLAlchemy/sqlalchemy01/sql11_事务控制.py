#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/12 16:02
# Module    : sql11_事务控制.py
# explain   : 事务控制

from sql02_database_async_connect import *

from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, Query, Depends, HTTPException, Body
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, update, select, Sequence, func
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import declarative_base, Session
from typing import Annotated, List, Dict, Optional
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    # SQLAlchemy 会记录 User 的元信息，存放在 Base.metadata 里
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

import time


async def session_test1(user: User):
    async with AsyncSessionLocal() as session:
        session.add(user)

        # 使用session的方式必须手动提交事务，如果不使用 session.commit() 的话，那么这条语句的执行结果不会被提交到数据库
        await session.commit()


# 自定义一个事务管理函数 get_session
# 支持自动开启session、自动提交事务以及自动回滚事务
@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            # yield 关键字会返回后面的数据，并且之后会继续执行 yield 后面的代码
            # 暂停函数执行，并把当前值“产出”，下次从暂停的地方继续执行
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise

async def session_test2(user: User, cond: int):
    async with get_session() as session:
        session.add(user)
        if cond and cond == -1:
            # 模拟异常发送
            print(1 / 0)

    pass



# 初始化数据库
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("="*10 + "init db success" + "="*10)

# 基于fastapi的 Lifespan 上下文管理器来执行 sqlalchemy 的异步事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动数据库
    await init_db()
    # 等待停止
    yield
    # 当fastapi被关闭的同时关闭数据库
    await engine.dispose()
    print("db closed!!!")


app = FastAPI(lifespan=lifespan)

@app.get("/api_session_test1")
async def api_session_test1():
    now_ts = int(time.time_ns())
    name = f"zhangsan-1-{now_ts}"
    user1 = User(name=name)
    await session_test1(user1)
    print(f"user_id: {user1}")
    return {
        "now_ts": now_ts,
        "data": user1
    }

@app.get("/api_session_test2")
async def api_session_test2(cond: Annotated[int, Query()]):
    now_ts = int(time.time_ns())
    name = f"zhangsan-api_session_test2-{now_ts}"
    user = User(name=name)
    await session_test2(user, cond)
    print(f"user_id: {user}")
    return {
        "now_ts": now_ts,
        "data": user
    }
