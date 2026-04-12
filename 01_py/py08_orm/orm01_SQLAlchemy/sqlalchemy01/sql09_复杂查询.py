#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/12 16:03
# Module    : sql10_关系加载策略.py
# explain   : sqlalchemy复杂查询

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Query, HTTPException, status, APIRouter, Body
from typing import Optional, Annotated

from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, select, ForeignKey, Table, Sequence
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import declarative_base, Mapped, relationship, selectinload, contains_eager

from sql02_database_async_connect import MYSQL_ASYNC_ENGINE, MYSQL_ASYNC_AsyncSessionLocal

engine:AsyncEngine = MYSQL_ASYNC_ENGINE
AsyncSessionLocal = MYSQL_ASYNC_AsyncSessionLocal


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    roles = relationship(
        "Role",
        secondary="user_roles",
        backref="users"
    )

class UserRole(Base):
    __tablename__ = "user_roles"
    # 类似这种两张表的中间表，如果设计的时候两个字段都不是主键，
    # 但是此时，sqlalchemy的Model定义又必须要有 primary_key=True 那么此时就必须两个都设置 primary_key=True 防止程序启动报错
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, primary_key=True)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    tag = Column(String(50), nullable=False)

# 初始化数据库
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("="*10 + "init db success" + "="*10)


# 实现多表join查询
async def select_user_roles(user: User, role: Role) -> Sequence[User]:
    async with get_session(AsyncSessionLocal) as session:
        stmt = (select(User)
                .join(UserRole, User.id == UserRole.user_id)
                .join(Role, UserRole.role_id == Role.id)
                .where(User.id == user.id)
                .distinct()  # 给user.id去重
        )
        print("role", role)
        if role.tag:
            print("role.tag", role.tag)
            stmt = stmt.where(Role.tag == role.tag)

        # 一个 stmt 语句只能有一个 options 操作
        # stmt = stmt.options(selectinload(User.roles)).options(contains_eager(User.roles))  # 🔥 关键
        stmt = stmt.options(contains_eager(User.roles))  # ✅ 只保留这个

        r = await session.execute(stmt)
        # 假设：user1 → roleA, roleB
        # SQL 结果会是：
        # user1 + roleA
        # user1 + roleBuser1 → roleA, roleB
        #
        # SQL 结果会是：
        # user1 + roleA
        # user1 + roleB
        # 因此必须加载 unique() 函数
        res = r.scalars().unique().all()
        print(res)
        return res



# 实现数据库方法
@asynccontextmanager
async def get_session(SessionLocal):
    """
    get_session
        支持自动管理事务
    """
    async with SessionLocal() as session:  # type: AsyncSession
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_user(id: int) -> User:
    async with get_session(AsyncSessionLocal) as session:  # type: AsyncSession
        # 要在查询时显式告诉 SQLAlchemy：把 profile 一起查出来
        stmt = select(User)
        if id > 0:
            stmt = stmt.where(User.id == id)
        res = await session.execute(stmt)
        user: Optional[User] = res.scalars().first()
        return user



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



# curl -X 'GET' \
#   'http://127.0.0.1:9002/getInfo?user_id=1&tag=pt' \
#   -H 'accept: application/json'
@app.get("/getInfo")
async def get_user_info(user_id: Annotated[int, Query()], tag: Annotated[str, Query()] = None):
    print(f"user_id: {user_id}")
    user = await select_user_roles(User(id = user_id), Role(tag = tag))
    return {
        "user_id": user_id,
        "data": user
    }


