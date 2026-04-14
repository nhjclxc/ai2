# 加载模块即可，无须进行其他操作
import time

import pkg.web_fastapi as _

from contextlib import asynccontextmanager

from api.global_exception import register_exception
from middleware.token_middleware import get_current_user
from pkg.db_msqyl import init_db, get_engine
from api.admin.user_api import user_router
from fastapi.middleware.cors import CORSMiddleware
from middleware.logging_middleware import logging_middleware

from fastapi import FastAPI, APIRouter, Request, Depends


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



app = FastAPI(lifespan=lifespan)

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_user)],
)


admin_router.include_router(user_router)

app.include_router(admin_router)

# 给 app 注册全局异常处理
register_exception(app)

# 支持跨域
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册中间件
app.middleware("http")(logging_middleware)

# fastapi dev .\main.py --port=6001

