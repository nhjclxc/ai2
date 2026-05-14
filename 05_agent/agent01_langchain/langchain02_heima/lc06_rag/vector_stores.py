#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/11 21:40
# Module    : vector_stores.py
# explain   : 向量库检索器类

# 当前文件废弃，直接使用 knowledge_base.py 的 get_retriever 方法

from langchain_core.vectorstores import InMemoryVectorStore, VectorStoreRetriever

from langchain02_heima.lc06_rag.config_data import embed_model


class VectorStoreService:

    def __init__(self):
        self.vector_store = InMemoryVectorStore(embed_model)

    def get_retriever(self) -> VectorStoreRetriever:
        return self.vector_store.as_retriever(k=5)