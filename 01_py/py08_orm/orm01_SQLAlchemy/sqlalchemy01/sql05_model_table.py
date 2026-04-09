
# 模型和表
# https://sqlalchemy.flask.org.cn/en/3.1.x/models/


"""
CREATE TABLE `users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `age` INT NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

import asyncio
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, select, update, delete
import sqlalchemy

# 1️⃣ 异步 MySQL 连接
from sql02_database_async_connect import MYSQL_ASYNC_ENGINE, MYSQL_ASYNC_AsyncSessionLocal

engine:AsyncEngine = MYSQL_ASYNC_ENGINE
AsyncSessionLocal = MYSQL_ASYNC_AsyncSessionLocal

# declarative_base() 创建了一个 基类 Base
# 所有继承 Base 的类（你的 User）都会被 SQLAlchemy ORM 注册
# SQLAlchemy 内部会把 User、Order 类的 类属性（Column） → 映射成数据库表的字段
Base = declarative_base()

# 2️⃣ 定义 ORM Model
class User(Base):
    __tablename__ = "users"
    # SQLAlchemy 会记录 User 的元信息，存放在 Base.metadata 里
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)

# 3️⃣ 初始化表（创建表）
async def init_db():
    async with engine.begin() as conn:
        # 这一步会创建所有继承了 Base 的表
        await conn.run_sync(Base.metadata.create_all)
    print("✅ tables created")

from typing import cast
# 4️⃣ CRUD 示例
async def create_user(name: str, age: int):
    async with AsyncSessionLocal() as session:
        session = cast(AsyncSession, session)
        new_user = User(name=name, age=age)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)  # 获取最新数据
        return new_user

async def get_user_by_id(user_id: int) -> User:
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

async def update_user_age(user_id: int, new_age: int):
    async with AsyncSessionLocal() as session:
        session: AsyncSession = session
        await session.execute(update(User).where(User.id == user_id).values(age=new_age))
        await session.commit()

async def delete_user(user_id: int):
    async with AsyncSessionLocal() as session:
        await session.execute(delete(User).where(User.id == user_id))
        await session.commit()

        # await session.delete(User(id = user_id))
        # await session.execute(delete(User).where(User.id == user_id))
        # | 方法                                         | 使用场景                      | 备注              |
        # | ------------------------------------------ | ------------------------- | --------------- |
        # | `session.delete(obj)`                      | 删除单个对象，或者需要触发 ORM 事件、级联删除 | 对象已经在 session 中 |
        # | `session.execute(delete(User).where(...))` | 批量删除、按条件删除，不需要查询对象        | 更接近 SQL，性能高     |

        pass

async def list_users() -> Sequence[User]:
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        result = await session.execute(select(User))
        return result.scalars().all()


# 使用上下文管理器封装自动提交（推荐）
from contextlib import asynccontextmanager
@asynccontextmanager
async def get_session(auto_commit: bool = True):
    async with AsyncSessionLocal() as session:
        try:
            yield session
            if auto_commit:
                await session.commit()  # 自动提交
        except Exception:
            await session.rollback()  # 出错回滚
            raise

async def create_user2(name: str, age: int):
    async with get_session() as session:
        user = User(name=name, age=age)
        session.add(user)
        # 不需要手动 commit
        return user
#
# def auto_commit(func):
#     async def wrapper(*args, **kwargs):
#         async with get_session() as session:
#             return await func(session, *args, **kwargs)
#     return wrapper
#
# @auto_commit
# async def add_user(session: AsyncSession, name: str, age: int):
#     user = User(name=name, age=age)
#     session.add(user)
#     return user

# 5️⃣ 测试 CRUD
async def main():
    await init_db()

    # Create
    await create_user("zhangsan", 18)
    await create_user("lisi", 28)
    user = await create_user("Alice", 20)
    print("Created:", user.id, user.name, user.age)

    await create_user2("user.name", 111)
    # await add_user(session=AsyncSessionLocal, name="z1111hangsan", age=18)

    # Read
    user = await get_user_by_id(user.id)
    print("Fetched:", user.id, user.name, user.age)

    # Update
    await update_user_age(user.id, 25)
    user = await get_user_by_id(user.id)
    print("Updated:", user.id, user.name, user.age)

    # List
    users = await list_users()
    print("All users:", [(u.id, u.name, u.age) for u in users])

    # Delete
    await delete_user(user.id)
    users = await list_users()
    print("After deletion:", [(u.id, u.name, u.age) for u in users])

    # 安全关闭连接池
    await engine.dispose()

asyncio.run(main())










