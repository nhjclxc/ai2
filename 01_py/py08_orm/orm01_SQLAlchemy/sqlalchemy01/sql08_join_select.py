#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/11 08:16
# Module    : sql08_join_select.py
# explain   : 实现表的关联查询，包含一对一，一对多，多对多
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Query, HTTPException, status, APIRouter, Body
from typing import Optional, Annotated

from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, select, ForeignKey, Table
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import declarative_base, Mapped, relationship, selectinload

from sql02_database_async_connect import MYSQL_ASYNC_ENGINE, MYSQL_ASYNC_AsyncSessionLocal

engine:AsyncEngine = MYSQL_ASYNC_ENGINE
AsyncSessionLocal = MYSQL_ASYNC_AsyncSessionLocal


Base = declarative_base()


# 定义多对多（User ↔ Role）的中间件表 user_roles
user_roles = Table(
    "user_roles",
    Base.metadata,
Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("role_id", Integer, ForeignKey("roles.id"), nullable=False)
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    # 实现一对多（User ↔ Message）
    #
    # Mapped映射里面的字符串是类名，不是表名
    # relationship 是定义两个表User 和 Profile直接的关联关系
    #   uselist=False：表示关联查询返回的结果要不要使用list，False表示不使用list返回，也就是一对一的关系
    profile: Mapped["Profile"] = relationship(uselist=False)


    # 实现一对多（User ↔ Message）
    messages = relationship("Message", uselist=True)

    # 实现 多对多（User ↔ Role） user_role
    roles = relationship("Role",secondary=user_roles,back_populates="users")

    pass

# 1️⃣ 一对多（User ↔ Message）
class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 必须指定 user_id 是哪个表的主键，即在这里就是指定profile的关联外键，注意：这里使用的是表名.表的列名
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    age = Column(Integer, nullable=True)
    addr = Column(String(50), nullable=False)

    # 实现user与profile的一对一查询，一般要用子查父的时候使用
    # user: Mapped["User"] = relationship()

# 2️⃣ 一对多（User ↔ Message）
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String(100), nullable=False)

# 3️⃣ 多对多（User ↔ Role）
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    tag = Column(String(50), nullable=False)

    users: Mapped[list["User"]] = relationship(
        secondary=user_roles,
        back_populates="roles"
    )


# 初始化数据库
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("="*10 + "init db success" + "="*10)

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


async def create_user(user: User) -> User:
    async with get_session(AsyncSessionLocal) as session:  # type: AsyncSession
        print("create_user session ", user)
        # cascade="save-update", 会自动INSERT user， INSERT profile
        session.add(user)
        await session.commit()
        # 要想可以立即去调用数据库，那么必须先提交事务
        await session.refresh(user)
        print(f"create user result id {user.id}")
        # 级联创建 profie
        # profile = await create_profile(user.profile)
        # user.profile = profile
        return user


async def create_profile(profile: Profile) -> Profile:
    async with get_session(AsyncSessionLocal) as session:  # type: AsyncSession
        session.add(profile)
        await session.commit()
        await session.refresh(profile)
        print(f"create profile result id {profile.id}")
        return profile



async def get_user(id: int) -> User:
    async with get_session(AsyncSessionLocal) as session:  # type: AsyncSession
        # 要在查询时显式告诉 SQLAlchemy：把 profile 一起查出来
        stmt = select(User).options(
            selectinload(User.profile),  # ✅ 关键
            selectinload(User.messages),  # ✅ 关键
            selectinload(User.roles),  # ✅ 关键
        )
        if id > 0:
            stmt = stmt.where(User.id == id)
        res = await session.execute(stmt)
        user: Optional[User] = res.scalars().first()
        return user

async def get_profile(id: int) -> Optional[Profile]:
    async with get_session(AsyncSessionLocal) as session:  # type: AsyncSession
        stmt = select(Profile)
        if id > 0:
            stmt = stmt.where(Profile.id == id)
        res = await session.execute(stmt)
        profile: Optional[Profile] = res.scalars().first()
        return profile



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


admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

class RequestProfile(BaseModel):
    id: int | None = Field(default=None)
    user_id: int | None = Field(default=None)
    age: int
    addr: str

class RequestUser(BaseModel):
    id: int | None = Field(default=None)
    name: str
    profile: Optional[RequestProfile]

    def to_orm(self) -> User:
        user_dict = self.model_dump()
        print("user_dict", user_dict)
        profile = Profile(**user_dict['profile'])
        return User(id=user_dict['id'], name=user_dict['name'], profile=profile)


@user_router.post("/create")
async def create_user_api(request_user: Annotated[RequestUser, Body()]):
    print(f"request user: {request_user}")
    user = request_user.to_orm()
    print(f"user: {user}")
    user_db = await create_user(user)
    return {
        "id": user_db.id,
        "user": user_db,
    }


# 实现 user 与 profile 一对一查询
@user_router.get("/getInfo")
async def get_user_info(user_id: Annotated[int, Query()]):
    print(f"user_id: {user_id}")
    user = await get_user(user_id)
    return {
        "user_id": user_id,
        "data": user
    }

@user_router.get("/getProfile")
async def get_user_profile(profile_id: Annotated[int, Query()]):
    print(f"profile_id: {profile_id}")
    profile = await get_profile(profile_id)
    return {
        "profile_id": profile_id,
        "data": profile
    }



admin_router.include_router(user_router)

app.include_router(admin_router)


