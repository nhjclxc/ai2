
# sql02_database_async_connect.py
# 建立数据库的异步连接，适于用 fastapi 使用



from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import sqlalchemy

# 异步连接字符串
# 同步驱动使用：pymysql，异步驱动使用：aiomysql
# DATABASE_URL = "mysql+pymysql://root:root123@localhost:3306/mysqldb?charset=utf8mb4"
DATABASE_URL = "mysql+aiomysql://root:root123@localhost:3306/mysqldb?charset=utf8mb4"

# 创建异步 Engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)

# 异步 Session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

if __name__ == "__main__":
    # 异步操作示例
    import asyncio
    async def test_async_mysql():
        async with AsyncSessionLocal() as session:
            result = await session.execute(sqlalchemy.text("SELECT VERSION();"))
            version = result.fetchone()
            print("MySQL version:", version[0])
        await engine.dispose()  # 关闭连接池

    asyncio.run(test_async_mysql())

MYSQL_ASYNC_ENGINE = engine
# MYSQL_ASYNC_AsyncSessionLocal = AsyncSessionLocal
MYSQL_ASYNC_AsyncSessionLocal = AsyncSessionLocal



# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase
#
# class Base(DeclarativeBase):
#   pass
#
# db = SQLAlchemy(model_class=Base)
# from sqlalchemy import Integer, String
# from sqlalchemy.orm import Mapped, mapped_column
#
# class User(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     username: Mapped[str] = mapped_column(unique=True)
#     email: Mapped[str]