#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:08
# Module    : constants.py
# explain   :


from app.exceptions.business_exception import BusinessException

user_age_required_over_18 = BusinessException(50001, "用户年龄必须大于18")
user_name_len_required_over_6 = BusinessException(50002, "用户名称必须大于6个字符")