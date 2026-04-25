


init project

```shell

## 1️⃣ 初始化项目
uv init project03_lucky_draw
cd project03_lucky_draw
## 2️⃣ 创建虚拟环境
uv venv
## 3️⃣ 激活环境
# Windows 
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
## 4️⃣ 安装依赖
### web
pip install "fastapi[standard]" uvicorn
uv add "fastapi[standard]" uvicorn
uv add flask flask_sqlalchemy
### db
uv add redis sqlalchemy pymysql mysqlclient aiomysql greenlet alembic
### token
uv add "python-jose" "passlib[bcrypt]"
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

uvicorn app.main:app --reload --port 8001