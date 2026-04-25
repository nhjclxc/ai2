#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:09
# Module    : business_exception.py
# explain   :


class BusinessException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
        super().__init__(msg)