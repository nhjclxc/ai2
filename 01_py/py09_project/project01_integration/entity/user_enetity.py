#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/13 22:08
# Module    : user_enetity.py
# explain   :
from pydantic import BaseModel, Field

from model.user import User


class RequestUser(BaseModel):
    # 如果允许字段为空，那么必须使用以下方法 | None = Field(default=None)
    id: int | None = Field(default=None)
    name: str | None = Field(default=None)

    # 实现分页查询
    page_num: int = Field(default=1)
    page_size: int = Field(default=10)

    def to_orm(self) -> User:
        # entity 与 model 的字段一摸一样时使用以下方法即可
        # return User(**self.model_dump())
        # 当 entity 与 model 的字段有差异时，使用以下方法
        user_dict = self.model_dump()
        # 如果user model里面没有的字段要移除
        user_dict.pop("page_num")
        user_dict.pop("page_size")
        return User(**user_dict)

class UserResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # ✅ 关键
