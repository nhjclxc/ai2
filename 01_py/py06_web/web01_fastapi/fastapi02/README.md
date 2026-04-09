
# FASTAPI



uv venv .venv

Windows 激活uv虚拟环境：.venv\Scripts\activate.bat
Linux/macOS 激活uv虚拟环境：source .venv/bin/activate

`uv pip install "fastapi[standard]"`（标准版）
`uv pip install "uvicorn"`

uv pip freeze > requirements.txt

uv pip install -r requirements.txt