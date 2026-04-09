

from fastapi import FastAPI, Depends
from typing import Annotated


from pydantic import BaseModel

# 使用表单模型来接收参数
class UserLogin(BaseModel):
    username: str
    password: str


app = FastAPI()


@app.post("/f20/login", response_model=UserLogin)
def login(form: UserLogin):
    print("login:", form)
    return form


from fastapi.security import OAuth2PasswordBearer

# 表示从请求头中获取token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# curl -H "Authorization: Bearer abc123" http://127.0.0.1:8000/f20/token
@app.get("/f20/token")
async def read_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}







# pip install "python-jose" "passlib[bcrypt]"

from datetime import datetime, timedelta
from jose import jwt
from jose import JWTError


SECRET_KEY = "your-secret-key"  #
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def generate_token(data: dict) -> str:
    """ 生成token， data就是载核 """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

if __name__ == "__main__":
    data = {
        "username": "admin",
    }

    token = generate_token(data)
    print(token)

    payload = verify_token(token)
    if payload:
        print(f"payload: {payload}")
    else:
        print("token无效")

    token2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNzc1NjM3NzA0fQ.hNnXvlWWuuIP4T_ISuplixs7RgS7gJ4pdW-8n5DmfS0"
    payload = verify_token(token2)
    if payload:
        print(f"payload: {payload}")
    else:
        print("token无效")






