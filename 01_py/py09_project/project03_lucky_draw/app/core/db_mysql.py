#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:03
# Module    : db_mysql.py
# explain   : 初始化 mysql 数据库

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
    print("init db")
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("init db success")


@asynccontextmanager
async def get_session(async_session):
    """
    get_session
        支持自动管理事务

    用法
        async with get_session(get_async_session_local()) as session:  # type: AsyncSession

    """
    async with async_session() as session:  # type: AsyncSession
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


"""

# 使用 sqlalchemy 的数据库迁移工具 Alembic 对数据库实现迁移
# 以达到 数据库中存在某些表了，但是我们在类中修改了字段，也可以同步给数据库的需求

1、安装 Alembic：uv add alembic
2、初始化 Alembic
    在项目根目录执行：alembic init alembic
3、编辑 alembic.ini 配置数据库链接，修改【sqlalchemy.url】这一项，注意；必须使用同步驱动pymysql
    sqlalchemy.url=mysql+pymysql://root:root123@localhost:3306/mysqldb?charset=utf8mb4
    
4、编辑 alembic/env.py 以绑定 orm
    4.1、导入Base：from app.core.db_mysql import Base
    4.2、设置 metadata：target_metadata = Base.metadata
    4.3、加载所有数据库模型：
        4.3.1、在 models包下将所有的model实体添加到 __init__.py 文件里面
        4.3.2、并将所有的模块文件和所有的模型类导出，详细看 __init__.py 的编写
5、生成迁移脚本（以后每次修改了某个类的字段直接执行下面的即可）
    以下假设给 User 里面增加了一个 vip = Column(Boolean, nullable=False, default=False) 的字段，那么以下进行演示
    执行第一步：根目录执行：alembic revision --autogenerate -m "add vip to user"，这时会生成一个文件：`alembic/versions/xxx_add_vip_to_user.py`
    执行第二步：执行数据库迁移：alembic upgrade head
    
    
(project03_lucky_draw) PS D:\code\py\ai2\01_py\py09_project\project03_lucky_draw> alembic revision --autogenerate -m "add vip to user"
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.schemas
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.tables
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.types
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.constraints
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.defaults
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.comments
Creating directory D:\code\py\ai2\01_py\py09_project\project03_lucky_draw\alembic\versions ...  done
Generating D:\code\py\ai2\01_py\py09_project\project03_lucky_draw\alembic\versions\adb10c0dac9e_add_vip_to_user.py ...  done
(project03_lucky_draw) PS D:\code\py\ai2\01_py\py09_project\project03_lucky_draw> alembic upgrade head
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> adb10c0dac9e, add vip to user

"""







