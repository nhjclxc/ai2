#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:05
# Module    : prize.py
# explain   :
from pydantic import BaseModel, Field

from app.models.user import User


class CreateUserRequest(BaseModel):
    name: str | None = Field(default=None)
    age: int | None = Field(default=None)

    def to_orm(self) -> User:
        # entity 与 model 的字段一摸一样时使用以下方法即可
        # return User(**self.model_dump())
        # 当 entity 与 model 的字段有差异时，使用以下方法
        user_dict = self.model_dump()
        # 如果user model里面没有的字段要移除
        # user_dict.pop("page_num")
        # user_dict.pop("page_size")
        return User(**user_dict)



