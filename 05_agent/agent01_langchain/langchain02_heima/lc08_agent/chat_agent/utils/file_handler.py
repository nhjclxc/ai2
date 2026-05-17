#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/16 16:47
# Module    : file_handler.py
# explain   : 文件处理函数
import hashlib
import os
from pathlib import Path
from typing import Any, Generator

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from langchain02_heima.lc08_agent.chat_agent.utils.logger_handler import logger
from langchain02_heima.lc08_agent.chat_agent.utils.path_tool import exists, get_abs_path


def read_file(path: str) -> str:
    """ 读取文本文件数据 """
    abs_path = get_abs_path(path)
    if not os.path.exists(abs_path):
        logger.error(f" read_file {abs_path} 不存在")
        return ""
    if not os.path.isfile(abs_path):
        logger.error(f" read_file {abs_path} 不是文件")
        return ""

    with open(abs_path, 'rb') as f:
        bytes = f.read()
        return str(bytes, 'utf-8')

def save_file(path: str, data: str):

    abs_path = get_abs_path(path)
    if not os.path.exists(abs_path):
        logger.error(f" read_file {abs_path} 不存在")
    if not os.path.isfile(abs_path):
        logger.error(f" read_file {abs_path} 不是文件")

    with open(abs_path, 'a', encoding='utf-8') as f:
        f.write(data)


def read_file_stream(path: str) -> Generator[bytes, Any, str | None]:
    """ 流式读取文本文件数据 """
    abs_path = get_abs_path(path)
    if not os.path.exists(abs_path):
        logger.error(f" read_file {abs_path} 不存在")
        return ""
    if not os.path.isfile(abs_path):
        logger.error(f" read_file {abs_path} 不是文件")
        return ""

    chunk_size = 4096
    try:
        with open(abs_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                yield chunk
    except Exception as e:
        logger.error(f"read_file_stream {abs_path} 获取文件md5失败： {str(e)}")


def get_file_md5(path: str) -> str:
    """ 获取文件md5值 """

    data = read_file(path)
    print('data ', data)
    if data == "":
        return ""
    return get_text_md5(data)


def get_file_stream_md5(path: str) -> str:
    """ 获取文件md5值 """

    md5_obj = hashlib.md5()

    for chunk in read_file_stream(path):
        md5_obj.update(chunk)
    return md5_obj.hexdigest()



def get_text_md5(text: str) -> str:
    """ 获取文本md5值 """
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def _str_prefix_add_dot(input: str) -> str:
    if input[0] == '.':
        return input
    return '.' + input

def list_dir_with_allowed_types(path, types) -> list:
    """
        返回某个路径下指定类型的所有文件后缀文件列表
    """

    if types == "":
        return []


    pathlib_path = Path(get_abs_path(path))
    if not os.path.isdir(pathlib_path):
        logger.error(f"pathlib_path: {pathlib_path} 不是文件夹 ")
        return []

    allowed_types = []
    if type(types) == str:
        allowed_types.append(_str_prefix_add_dot(types.lower()))
    elif type(types) == list:
        for t in types:
            allowed_types.append(_str_prefix_add_dot(t.lower()))
    else:
        raise TypeError("allowed_types should be str or list")


    allowed_file_paths = []
    for file in pathlib_path.iterdir():
        if file.is_file() and file.suffix.lower() in allowed_types:
            allowed_file_paths.append(file)

    return allowed_file_paths


def pdf_loader(path: str, pwd: str = None) -> list[Document]:
    """
        获取 path 对应的pdf文件数据
    :param path: 传入文件的绝对路径
    :param pwd: 密码
    :return: 返回文件的所有文本数据
    """

    loader = PyPDFLoader(
        file_path=path,
        password=pwd,
    )

    return loader.load()


def txt_loader(path: str) -> list[Document]:
    """
        获取 path 对应的 txt 文件数据
    :param path: 传入文件的绝对路径
    :return: 返回文件的所有文本数据
    """

    loader = TextLoader(
        file_path=path,
        encoding="utf-8",
    )

    return loader.load()


prompt_rag_summarize = read_file(get_abs_path("prompt/rag_summarize.txt"))
prompt_main_prompt = read_file(get_abs_path("prompt/main_prompt.txt"))
prompt_report_prompt = read_file(get_abs_path("prompt/report_prompt.txt"))


if __name__ == '__main__':

    # print(get_text_md5("hello"))
    # print(get_text_md5("world"))
    # print(get_file_md5("utils/text.txt"))

    # print(len(list_dir_with_allowed_types("data", ".txt")))
    # print(len(list_dir_with_allowed_types("data", [".txt", "csv"])))
    # print(len(list_dir_with_allowed_types("data", [".txt", "csv", ".pdf"])))

    # txt_file_path = list_dir_with_allowed_types("data", ".txt")[0]
    # print(txt_file_path)
    # print(txt_loader(txt_file_path))

    # pdf_file_path = list_dir_with_allowed_types("data", ".pdf")[0]
    # print(pdf_file_path)
    # print(pdf_loader(pdf_file_path))


    print(read_file(get_abs_path("prompt/rag_summarize.txt")))



    pass