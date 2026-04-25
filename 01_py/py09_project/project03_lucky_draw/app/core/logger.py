#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/22 21:04
# Module    : logger.py
# explain   :

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    # filename="app.log"
)

logging.info("hello logging")

# 对外提供日志对象
logger = logging

