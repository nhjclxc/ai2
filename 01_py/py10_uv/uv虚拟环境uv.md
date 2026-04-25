

```shell

## 1️⃣ 初始化项目
uv init py07_cache
cd py07_cache
## 2️⃣ 创建虚拟环境
uv venv
## 3️⃣ 激活环境
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
## 4️⃣ 安装依赖
uv add redis
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

```
## 1️⃣ 初始化项目
uv init myapp
cd myapp
## 2️⃣ 创建虚拟环境
uv venv
## 3️⃣ 激活环境
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
## 4️⃣ 安装依赖
uv add fastapi
## 5️⃣ 运行代码
uv run python main.py
```




下面给你一套**从入门 → 进阶 → 实战 → 生产级**的完整指南，围绕 uv 的真实使用场景来讲（不是零碎命令，而是完整开发流程）。

---

# 🧭 一、uv 核心理念（先建立认知）

uv = **虚拟环境 + 依赖管理 + 锁版本 + 运行工具**

👉 类似于：

* Node.js 的 npm / pnpm
* Rust 的 cargo

---

# 🟢 二、入门：从 0 创建项目

## 1️⃣ 初始化项目

```bash
uv init myapp
cd myapp
```

生成：

```text
myapp/
├── pyproject.toml
├── README.md
```

---

## 2️⃣ 创建虚拟环境

```bash
uv venv
```

👉 会生成 `.venv/`

---

## 3️⃣ 激活环境（可选）

```bash
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

👉 ⚠️ 注意：**uv 不激活也能用**

---

## 4️⃣ 安装依赖

```bash
uv add fastapi uvicorn
```

👉 自动完成：

* 安装包
* 更新 `pyproject.toml`
* 生成 `uv.lock`

---

## 5️⃣ 运行代码

```bash
uv run python main.py
```

或：

```bash
uv run uvicorn app.main:app --reload
```

---

# 🟡 三、进阶：依赖管理（核心能力）

## 1️⃣ 添加依赖

```bash
uv add requests
```

指定版本：

```bash
uv add "requests==2.31.0"
```

---

## 2️⃣ 删除依赖

```bash
uv remove requests
```

---

## 3️⃣ 锁版本（生产关键）

```bash
uv lock
```

👉 生成：

```text
uv.lock
```

✔ 可复现环境
✔ 团队一致

---

## 4️⃣ 同步环境（部署用）

```bash
uv sync
```

👉 根据 lock 文件安装所有依赖

---

## 5️⃣ 查看依赖树

```bash
uv tree
```

---

# 🔵 四、虚拟环境深入理解

## 1️⃣ uv venv 本质

```bash
uv venv
```

≈

```bash
python -m venv .venv
```

👉 但 uv 做了优化：

* 更快
* 自动识别 Python 版本

---

## 2️⃣ 指定 Python 版本

```bash
uv venv --python 3.11
```

---

## 3️⃣ 使用系统 Python

```bash
uv python list
uv python install 3.12
```

👉 uv 可以管理 Python（很强）

---

# 🟣 五、开发效率技巧（非常实用）

## 1️⃣ 不激活环境直接运行

```bash
uv run python script.py
```

👉 不污染系统环境 👍

---

## 2️⃣ 临时运行（一次性依赖）

```bash
uv run --with requests python script.py
```

👉 不写入项目依赖

---

## 3️⃣ 运行 CLI 工具

```bash
uvx ruff check .
```

👉 类似 npx

---

## 4️⃣ 安装开发依赖

```bash
uv add --dev pytest ruff black
```

---

## 5️⃣ 分组依赖（进阶）

```bash
uv add --group dev pytest
```

---

# 🔴 六、实战项目（FastAPI 示例）

## 📁 结构

```text
my-fastapi/
├── .venv/
├── pyproject.toml
├── uv.lock
├── app/
│   ├── main.py
│   ├── config.py
│   └── api/
```

---

## 📌 安装依赖

```bash
uv add fastapi uvicorn pydantic-settings
```

---

## 📌 main.py

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "hello uv"}
```

---

## 📌 启动

```bash
uv run uvicorn app.main:app --reload
```

---

# 🟤 七、环境变量管理（生产必备）

## 1️⃣ 安装

```bash
uv add python-dotenv
```

---

## 2️⃣ 创建 `.env`

```env
APP_NAME=uv-demo
DEBUG=true
```

---

## 3️⃣ 使用

```python
import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("APP_NAME"))
```

---

# ⚫ 八、测试 + 代码质量（工程化）

## 安装工具

```bash
uv add --dev pytest ruff black
```

---

## 运行测试

```bash
uv run pytest
```

---

## 代码检查

```bash
uvx ruff check .
```

---

# 🟠 九、部署 & CI/CD（重点）

## 1️⃣ 生产安装

```bash
uv sync --frozen
```

👉 保证和 lock 完全一致

---

## 2️⃣ Docker 推荐

```dockerfile
FROM python:3.12

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync --frozen

CMD ["uv", "run", "uvicorn", "app.main:app"]
```

---

# 🧠 十、常见坑（你一定会遇到）

## ❌ 坑1：以为必须 activate

👉 不需要：

```bash
uv run python xxx.py
```

---

## ❌ 坑2：用 pip 安装

👉 会破坏依赖管理

正确：

```bash
uv add xxx
```

---

## ❌ 坑3：没提交 lock 文件

👉 必须提交：

```text
uv.lock
```

---

## ❌ 坑4：环境变量读取不到

👉 用 `.env` 或系统变量（你前面刚踩过）

---

# 🏁 十一、从入门到精通路线（给你规划好）

## 🟢 初级

* uv init
* uv venv
* uv add
* uv run

---

## 🟡 中级

* uv lock / sync
* dev 依赖
* uvx 工具

---

## 🔵 高级

* Python 多版本管理
* CI/CD
* Docker
* 依赖分组

---

## 🔴 专家

* monorepo
* 私有源
* 构建发布包
* 替代 poetry/pip-tools

---

# 🎯 最终总结

👉 uv 的本质优势：

* 🚀 极快（碾压 pip）
* 📦 一体化（替代 venv + pip）
* 🔒 可复现（lock 文件）
* 🧠 更现代（接近 npm / cargo）

---

如果你下一步是做：

👉 **Agent / AI / FastAPI 项目**

我可以给你一套：

🔥「企业级 uv 项目模板（带日志 / 配置 / 分层架构 / Docker）」

直接可以上线那种。
