#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/14 21:06
# Module    : logger_handler.py
# explain   : 日志工具

import logging
import os

from langchain02_heima.lc08_agent.chat_agent.config.config import cfg
from langchain02_heima.lc08_agent.chat_agent.utils import path_tool



def get_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
        获取一个日志输出器
    """

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger


    # 关键
    logger.setLevel(level)

    filename = path_tool.get_abs_path(cfg.log.path)

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # 以下日志格式的时间格式如何设置为："%Y-%m-%d %H:%M:%S"
    log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
            "%Y-%m-%d %H:%M:%S"
    )

    # 控制台日志输出器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    # 设置文件日志输出器
    file_handler = logging.FileHandler(filename, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    return logger


logger = get_logger(__name__)


if __name__ == '__main__':
    logger.info("程序启动 __main__")

    logger.debug("debug日志")
    logger.info("info日志")
    logger.warning("warning日志")
    logger.error("error日志")

    pass