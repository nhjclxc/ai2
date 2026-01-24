#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/24 19:01
# Module    : base26.py
# explain   : logging日志模块，https://docs.python.org/zh-cn/3.10/library/logging.html

import logging

# 日志级别：
# logging.CRITICAL
# logging.ERROR
# logging.WARNING
# logging.INFO
# logging.DEBUG
# logging.NOTSET


# 默认的logging日志i输出级别是wraning,通过以下修改日志级别
# basicConfig 只能生效一次
logging.basicConfig(
    level=logging.NOTSET,
    format="自定义日志格式：%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),  # 控制台
        logging.FileHandler("app.log", encoding="utf-8")  # 文件
    ]
)

logging.critical("发生致命错误")  # 会导致程序停止，生产环境禁止使用
logging.error("error 日志")
logging.warning("wraning 日志")
logging.info("info 日志")
logging.debug("debug 日志")
logging.log(logging.NOTSET, "notest 日志")

# 以下是logger生产级别的日志使用模式
# 先获取日志对象
logger = logging.getLogger("myapp")
# 设置日志级别
logger.setLevel(logging.INFO)

# 1️⃣ 日志格式
fmt = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
)

# 2️⃣ 控制台 handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(fmt)

# 3️⃣ 文件 handler
file_handler = logging.FileHandler("app.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(fmt)

# 4️⃣ 绑定 handler
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 使用
logger.info("服务启动")
logger.warning("警告信息")
logger.error("错误信息")

"""
六、全局统一 logging（配置一次，全项目生效）
logging_config.py
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO"
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "app.log",
            "when": "D",
            "backupCount": 7,
            "formatter": "default",
            "encoding": "utf-8",
            "level": "INFO"
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO"
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

"""
