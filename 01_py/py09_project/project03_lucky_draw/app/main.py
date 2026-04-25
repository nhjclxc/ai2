from contextlib import asynccontextmanager


def main():
    print("Hello from project03-lucky-draw!")

import time
import json
from app.api.router import api_router
from app.core.logger import logger

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.db_mysql import init_db, get_engine
from app.exceptions.business_exception import BusinessException



# 基于fastapi的 Lifespan 上下文管理器来执行 sqlalchemy 的异步事件

# Lifespan 上下文管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动逻辑
    # 启动fastapi（web）的时候同时启动数据库（orm）
    await init_db()
    yield
    # 关闭逻辑（可选）
    await get_engine().dispose()
    print("✅ engine disposed")

app = FastAPI(
    title="抽奖系统",
    version="1.0.0",
    description="Lottery System API",
    lifespan=lifespan   # 👈 必须加这个
)

# 注册所有路由
app.include_router(api_router, prefix="/api/v1")


# 注册全局异常捕获器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content={
            "code": 500,               # 你自己的业务错误码
            "msg": str(exc),           # 异常信息
            "type": "系统异常",
            "data": None
        }
    )

# 注册业务异常捕获器
@app.exception_handler(BusinessException)
async def biz_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=200,
        content={
            "code": exc.code,
            "msg": exc.msg,
            "type": "业务异常",
            "data": None
        }
    )

# 注册全局请求日志打印器
@app.middleware("http")
async def log_middleware(request: Request, call_next):
    start_time = time.time()

    # ======================
    # 1️⃣ 读取请求信息
    # ======================
    try:
        body_bytes = await request.body()
        body = body_bytes.decode("utf-8")
    except Exception:
        body = "<cannot read body>"

    query_params = dict(request.query_params)

    # ⚠️ 重新注入 body（否则后续接口拿不到）
    async def receive():
        return {"type": "http.request", "body": body_bytes}

    request._receive = receive

    # ======================
    # 2️⃣ 执行请求
    # ======================
    response = await call_next(request)


    # 对响应数据不做处理，防止改变原有数据
    # # ======================
    # # 3️⃣ 读取响应数据
    # # ======================
    # resp_body = b""
    # async for chunk in response.body_iterator:
    #     resp_body += chunk
    #
    # content_type = response.headers.get("content-type", "")
    #
    # if "application/json" in content_type:
    #     try:
    #         content = json.loads(resp_body)
    #     except Exception:
    #         content = None
    # else:
    #     content = resp_body.decode("utf-8", errors="ignore")
    #
    # new_response = JSONResponse(
    #     content=content,
    #     status_code=response.status_code,
    #     headers=dict(response.headers)
    # )

    # ======================
    # 4️⃣ 打印日志
    # ======================
    process_time = round(time.time() - start_time, 4)

    request_info = {
        "method": request.method,
        "url": str(request.url),
        "query": query_params,
        "body": body,
        "status": response.status_code,
        # "response": resp_body.decode("utf-8"),
        "cost": process_time
    }
    logger.info(json.dumps(request_info, ensure_ascii=False))

    return response
# uvicorn app.main:app --reload --port 8001
