# ai2 - 01_py


# 创建虚拟环境并安装依赖
uv venv .venv
source .venv/bin/activate  # Linux/macOS
uv pip install -r requirements.txt
```

pip freeze | grep -v "file://" > requirements.txt



