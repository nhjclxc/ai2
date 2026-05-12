#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/10 22:17
# Module    : config_data.py
# explain   : 项目的一些配置

from lc00_core.model_helper import get_chat_openai, get_embedding_model



chat_model = get_chat_openai(streaming=True)

embed_model = get_embedding_model()


# 字符串md5数据存放位置
md5_file_path = ".\\data\\md5.txt"

collection_name = "KnowledgeBase"
persist_directory = ".\\data\\chroma_store"

# 文本分割最大阈值
max_split_char_number = 100

session_config = {"configurable": {"session_id": "session001"}}