
# sql01_database_connect.py
# 建立数据库连接

import sqlalchemy

# 1. 拼接连接字符串
# 前面的mysql是那种sql语言，后面的pymysql是使用什么驱动
# 格式: "mysql+pymysql://<username>:<password>@<host>:<port>/<database>?charset=utf8mb4"
DATABASE_URL = "mysql+pymysql://root:root123@localhost:3306/mysqldb?charset=utf8mb4"

# 2. 创建 Engine
engine = sqlalchemy.create_engine(
    DATABASE_URL,
    echo=True,      # 输出 SQL 调试信息
    pool_size=10,   # 连接池大小
    max_overflow=20 # 额外可创建的连接数
)

if __name__ == '__main__':
    # 3. 测试连接
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT VERSION();"))
        version = result.fetchone()
        print("MySQL version:", version[0])

MYSQL_ENGINE = engine



"""

2026-04-09 11:02:57,758 INFO sqlalchemy.engine.Engine SELECT DATABASE()
2026-04-09 11:02:57,758 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-04-09 11:02:57,759 INFO sqlalchemy.engine.Engine SELECT @@sql_mode
2026-04-09 11:02:57,759 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-04-09 11:02:57,759 INFO sqlalchemy.engine.Engine SELECT @@lower_case_table_names
2026-04-09 11:02:57,759 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-04-09 11:02:57,760 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-09 11:02:57,760 INFO sqlalchemy.engine.Engine SELECT VERSION();
2026-04-09 11:02:57,760 INFO sqlalchemy.engine.Engine [generated in 0.00008s] {}
MySQL version: 9.4.0
2026-04-09 11:02:57,760 INFO sqlalchemy.engine.Engine ROLLBACK

"""
