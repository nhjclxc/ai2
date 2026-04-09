

from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated


from pydantic import BaseModel


from fastapi02.f20_安全性 import generate_token, verify_token


# 使用表单模型来接收参数
class UserLogin(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    username: str
    age: int = 18


app = FastAPI()


@app.post("/f21/login")
def login(form: UserLogin):
    print("login:", form)
    token_paylaod = {"username": form.username}
    token = generate_token(token_paylaod)
    return {
        "code": 200,
        "data": {
            "token": f"Bearer {token}",
            "token_type": "bearer",
            "header": "Authorization",
        }
    }

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 写一个统一的鉴权方法
def common_verify_token(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInfo:
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_info = UserInfo(username=payload["username"])
    return user_info


# curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJuYW1lIiwiZXhwIjoxNzc1NjM4NjM3fQ.ud-cLKrYip9qDfLvCKR3KaHcuMLjmSrLRYsq1zFutGA" http://127.0.0.1:8000/f20/token

#  使用统一的鉴权方法
# 需要鉴权的接口就加上 user_info: Annotated[str, Depends(common_verify_token)]
@app.get("/f21/getInfo")
def get_info(user_info: Annotated[str, Depends(common_verify_token)]):
    print("get info:", user_info)
    return user_info

# 不需要鉴权的接口就不用加 user_info: Annotated[str, Depends(common_verify_token)]
@app.get("/f21/exec")
def get_info():
    print("get exec:", "")
    return {"code": 200}


# 以上方法没有使用路由分组，并且每一个接口都要加一次 user_info: Annotated[str, Depends(common_verify_token)] 很繁琐
# 高级用法使用APIRouter， 看 f22_安全性_APIRouter.py
