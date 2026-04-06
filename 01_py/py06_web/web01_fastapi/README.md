
# FASTAPI

## 文档
1. [fastapi官方](https://fastapi.org.cn/), [fastapi github](https://github.com/fastapi/fastapi)
2. [菜鸟教程](https://www.runoob.com/fastapi/fastapi-tutorial.html)
3. [fastapi示例教学](https://github.com/liaogx/fastapi-tutorial)

## 视频
1. [黑马程序员PythonWeb开发：FastAPI从入门到实战视频教程，涵盖路由、依赖注入、Pydantic、异步编程、ORM、项目拆分、模型训练、部署、接口测试](https://www.bilibili.com/video/BV1zV2QBtE39/)
   - 对应的资料：https://pan.baidu.com/s/1rvZVWcxYHTrRfiLBSCty3w&pwd=1234
_peng- 前端：https://gitee.com/deardhp/front-end-part-of-news-project.git和后端代码：https://gitee.com/deardhp/news-project.git




# 安装 FastAPI

## 安装
FastAPI：一般都是直接安装标准版
`pip install "fastapi[standard]"`（标准版）
`pip install fastapi`（阉割版）
`pip install "fastapi[all]"`（完整版）

👉 FastAPI ≠ Web服务器, FastAPI它只是框架，真正跑服务的是：Uvicorn 或 gunicorn 或 其他
FastAPI 本身不负责启动服务，需要一个服务，`pip install uvicorn`

## 示例代码

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}
```

## 启动一个FastAPI程序

启动命令，默认启动8000端口：

一个学习一般使用：fastapi dev main.py
```
(ai2) PS D:\code\py\ai2\01_py\py06_web\web01_fastapi> fastapi dev main.py

   FastAPI   Starting development server 🚀

             Searching for package file structure from directories with __init__.py files
             Importing from D:\code\py\ai2\01_py\py06_web\web01_fastapi

    module   🐍 main.py

      code   Importing the FastAPI app object from the module with the following code:

             from main import app

       app   Using import string: main:app

    server   Server started at http://127.0.0.1:8000
    server   Documentation at http://127.0.0.1:8000/docs

       tip   Running in development mode, for production use: fastapi run

             Logs:

      INFO   Will watch for changes in these directories: ['D:\\code\\py\\ai2\\01_py\\py06_web\\web01_fastapi']
      INFO   Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
      INFO   Started reloader process [25812] using WatchFiles
      INFO   Started server process [5268]
      INFO   Waiting for application startup.
      INFO   Application startup complete.

```


团队协同开发一般使用：`uvicorn main:app --reload`

```
(ai2) PS D:\code\py\ai2\01_py\py06_web\web01_fastapi> uvicorn main:app --reload    
INFO:     Will watch for changes in these directories: ['D:\\code\\py\\ai2\\01_py\\py06_web\\web01_fastapi']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [20200] using StatReload
INFO:     Started server process [26712]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

```

```
C:\Users\nhjcl>curl http://127.0.0.1:8000
{"message":"Hello FastAPI"}
C:\Users\nhjcl>curl http://127.0.0.1:8000/docs

    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <title>FastAPI - Swagger UI</title>
    </head>
    <body>
    
```


生产环境一般使用：`uvicorn main:app --host 0.0.0.0 --port 8000`
```
(ai2) PS D:\code\py\ai2\01_py\py06_web\web01_fastapi> uvicorn main:app --host 0.0.0.0 --port 8000
INFO:     Started server process [25792]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

```
