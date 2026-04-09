

import sqlalchemy
from sql01_database_connect import MYSQL_ENGINE
from sql02_database_async_connect import MYSQL_ASYNC_ENGINE, MYSQL_ASYNC_AsyncSessionLocal


# 测试连接
with MYSQL_ENGINE.connect() as conn:
    result = conn.execute(sqlalchemy.text("SELECT VERSION();"))
    version = result.fetchone()
    print("MYSQL_ENGINE MySQL version:", version[0])


# 异步操作示例
import asyncio
async def test_async_mysql():
    async with MYSQL_ASYNC_AsyncSessionLocal() as session:
        result = await session.execute(sqlalchemy.text("SELECT VERSION();"))
        version = result.fetchone()
        print("MYSQL_ASYNC_ENGINE MySQL version:", version[0])
    await MYSQL_ASYNC_ENGINE.dispose()  # 关闭连接池

asyncio.run(test_async_mysql())
