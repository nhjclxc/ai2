
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from pydantic import BaseModel


from f20_安全性 import generate_token, verify_token


# 使用表单模型来接收参数
class UserLogin(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    username: str
    age: int = 18


#  # tokenUrl 只是文档用途
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInfo:
    """
    从 Authorization: Bearer <token> 中解析用户信息
    """

    print("get_current_user:", token)
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(401, "Invalid token")
    return UserInfo(username=payload["username"], age=payload["age"] if "age" in payload else 28)

app = FastAPI()

# 要鉴权的路由
admin_api = APIRouter(
    prefix="/admin",
    tags=["admin"],
    # APIRouter上 [Depends(get_current_user)], 的作用：会对所有接口生效，但不传递返回值
    dependencies=[Depends(get_current_user)],
)

# 开放的路由
open_api = APIRouter(
    prefix="/open-api",
    tags=["openapi"],
)
open_api_v1 = APIRouter(
    prefix="/open-api/v1",
    tags=["open-api-v1"],
)
open_api_v2 = APIRouter(
    prefix="/open-api/v2",
    tags=["open-api-v2"],
)


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoyMTM2Mzc5ODYwfQ.hTQrBiY-Fuj0qVCxdvX1HrjGX8it5Gt7N80hMqeBFuY
# curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoyMTM2Mzc5ODYwfQ.hTQrBiY-Fuj0qVCxdvX1HrjGX8it5Gt7N80hMqeBFuY" http://127.0.0.1:8000/admin/userinfo
# 原来是直接使用 @app 现在使用路由分组了

# 使用APIRouter之后，路由的实际路径计算方式是：APIRouter.prefix + endpoint path
# 以下就是：/admin/userinfo
# 每个接口上的 Annotated[UserInfo, Depends(get_current_user)] 的作用：不仅会执行验证逻辑，而且可以把返回的 UserInfo 传给 endpoint。
# 所以如果你希望拿到当前用户信息，必须在 endpoint 上加一次 Depends。
# APIRouter就是解析当前用户的数据，而每个接口就是注入当前用户的数据
@admin_api.get("/userinfo")
async def userinfo(current_user: Annotated[UserInfo, Depends(get_current_user)]):
    print(f"current_user: {current_user}")
    return current_user


# curl http://127.0.0.1:8000/open-api/exec
@open_api.get("/exec")
async def open():
    print(f"open")
    return "open"

@open_api_v1.get("/open")
async def open_v1():
    print(f"open_v1")
    return "open_v1"



# 注意⚠️：必须先对具体的APIRouter添加路由，之后再使用app.include_router将APIRouter添加到@app上，顺序反了就不行了
# @open_api.get("/exec") 必须写在 app.include_router(open_api) 之前也可以，但逻辑上推荐先定义所有路由再 include。

# 使用 APIRouter 只是创建了 router，本身不会生效。
# 必须用 app.include_router(router) 才生效。
app.include_router(admin_api)
app.include_router(open_api)
open_api.include_router(open_api_v1)
open_api.include_router(open_api_v2)






