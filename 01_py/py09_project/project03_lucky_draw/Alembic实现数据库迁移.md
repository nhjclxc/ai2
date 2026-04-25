行，我直接给你一套**从 0 到能用的 Alembic 完整流程（适配 FastAPI + SQLAlchemy）**，包含命令 + 关键代码 + 常见坑。

你照着做，一次就能跑通。

---

# 🧱 一、安装

```bash
pip install alembic
```

---

# 🚀 二、初始化 Alembic

在**项目根目录**执行：

```bash
alembic init alembic
```

生成结构：

```bash
alembic/
├── versions/
├── env.py
├── script.py.mako
alembic.ini
```

---

# ⚙️ 三、配置数据库连接

编辑 `alembic.ini`：

```ini
sqlalchemy.url = mysql+pymysql://root:123456@127.0.0.1:3306/your_db
```

👉 ⚠️ 注意：

* 即使你项目用的是 `aiomysql`
* Alembic 也要用 **同步驱动（pymysql）**

---

# 🧩 四、绑定你的 ORM（关键步骤）

编辑：

```bash
alembic/env.py
```

---

## ✅ 1. 导入你的 Base

```python
from app.core.db_mysql import Base
```

---

## ✅ 2. 设置 metadata

找到：

```python
target_metadata = None
```

改成：

```python
target_metadata = Base.metadata
```

---

## ✅ 3. 确保加载所有模型（非常关键！）

👉 否则 autogenerate 检测不到表

```python
from app.models import user, activity, prize  # 👈 把所有 model import 进来
```

或者更优雅：

```python
import app.models  # 确保 __init__.py 里 import 了所有模型
```

---

# 🧠 五、确保 models 被注册（推荐写法）

## app/models/**init**.py

```python
from .user import User
from .activity import Activity
from .prize import Prize
```

👉 这样 Alembic 才能扫描到所有表

---

# 🧪 六、生成迁移脚本

## 场景：你给 User 加了字段

```python
email = Column(String(100))
```

执行：

```bash
alembic revision --autogenerate -m "add email to user"
```

---

## 📝 会生成文件：

```bash
alembic/versions/xxxx_add_email_to_user.py
```

内容类似：

```python
def upgrade():
    op.add_column('user', sa.Column('email', sa.String(length=100), nullable=True))

def downgrade():
    op.drop_column('user', 'email')
```

---

# 🚀 七、执行迁移

```bash
alembic upgrade head
```

👉 数据库表结构更新完成 ✅

---

# 🔁 八、以后流程（你只需要记住这个）

每次改模型：

```bash
alembic revision --autogenerate -m "描述"
alembic upgrade head
```

---

# 🔍 九、查看当前版本

```bash
alembic current
```

---

# ⏪ 十、回滚

```bash
alembic downgrade -1
```

或：

```bash
alembic downgrade base
```

---

# ⚠️ 十一、常见坑（你很可能会踩）

---

## ❌ 1. “没有生成变更”

原因：

👉 没 import models

解决：

```python
import app.models
```

---

## ❌ 2. JSON / Enum 不识别

你需要确保：

```python
from sqlalchemy import JSON, Enum
```

---

## ❌ 3. async engine 不能用

👉 Alembic 只能用同步连接（重点）

---

## ❌ 4. 字段 rename 不会识别

比如：

```python
name → username
```

👉 Alembic 会认为：

* drop column
* add column

需要手动改：

```python
op.alter_column(...)
```

---

# 🧱 十二、推荐项目结构（你现在就该这样改）

```bash
app/
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── activity.py
│   └── prize.py
├── core/
│   └── db_mysql.py
```

---

# 🔥 十三、进阶（自动创建数据库）

你可以在 `env.py` 加：

```python
from sqlalchemy import create_engine

engine = create_engine(config.get_main_option("sqlalchemy.url"))
conn = engine.connect()
conn.execute("CREATE DATABASE IF NOT EXISTS your_db")
conn.close()
```

---

# 🎯 最终总结（核心3步）

👉 你只要记住：

```bash
alembic revision --autogenerate -m "xxx"
alembic upgrade head
```

---

# 🚀 如果你想更进一步（强烈建议）

我可以帮你直接升级成：

* ✅ FastAPI + SQLAlchemy + Alembic 标准模板
* ✅ 自动迁移 + 多环境（dev/test/prod）
* ✅ Docker 一键启动数据库
* ✅ 避免“字段不同步 / 表结构错乱”问题

你后面做抽奖系统会轻松很多。
