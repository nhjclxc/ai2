#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/14 21:48
# Module    : token_middleware.py
# explain   :
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import time

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

#  # tokenUrl 只是文档用途
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LoginUserInfo(BaseModel):
    username: str
    age: int = 18

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> LoginUserInfo:
    """
    从 Authorization: Bearer <token> 中解析用户信息
    """

    print("get_current_user:", token)
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(401, "Invalid token")
    return LoginUserInfo(username=payload["username"], age=payload["age"] if "age" in payload else 28)


