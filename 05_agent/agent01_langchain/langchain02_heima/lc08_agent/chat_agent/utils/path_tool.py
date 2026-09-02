#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/14 20:48
# Module    : path_tool.py
# explain   : 获取项目的绝对路径

import os
import pathlib

def exists(path: str) -> bool:
    return

def get_project_root() -> pathlib.Path:
    """
        获取项目的根路径
    :return:
    """
    return pathlib.Path(__file__).resolve().parent.parent


def get_abs_path(relative_path: str) -> str:
    """
        根据相对路径，返回其绝对路径
    :param relative_path: 相对路径
    :return: 绝对路径
    """
    return os.path.join(get_project_root(), relative_path)


if __name__ == '__main__':

    print('当前项目的绝对路径：', get_project_root())

    print("相对路径测试：", get_abs_path("data\\rag_summarize.txt"))
    print("相对路径测试：", get_abs_path("config\\agent.yml"))



