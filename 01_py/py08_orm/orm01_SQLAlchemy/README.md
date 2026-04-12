

```
## 1️⃣ 初始化项目
uv init orm01_SQLAlchemy
cd orm01_SQLAlchemy
## 2️⃣ 创建虚拟环境
uv venv
## 3️⃣ 激活环境
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
## 4️⃣ 安装依赖
pip install "fastapi[standard]"
uv add uvicorn 
uv add flask flask_sqlalchemy
uv add sqlalchemy pymysql mysqlclient aiomysql greenlet
## 5️⃣ 运行代码
uv run python main.py
## 6️⃣ 输出当前依赖
uv pip freeze > requirements.txt
## 锁定依赖
uv lock
## 安装依赖
pip install -r requirements.txt
uv pip install -r requirements.txt
```







https://docs.sqlalchemy.org.cn/en/20/


https://sqlalchemy.flask.org.cn/en/3.1.x/



https://github.com/OpenDocCN/py-docs-zh/tree/master/docs/sqlalch_20


