#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/17 14:57
# Module    : rag_service.py
# explain   : rag 服务
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda

from langchain02_heima.lc08_agent.chat_agent.model.factory import chat_model
from langchain02_heima.lc08_agent.chat_agent.rag.vector_store import VectorStoreService
from langchain02_heima.lc08_agent.chat_agent.utils.file_handler import read_file



def print_prompt(x):
    print('='*60)
    print(x)
    print('='*60)
    return x

class RagService:

    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_template = PromptTemplate.from_template(read_file("prompt/rag_summarize.txt"))
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        return self.prompt_template | RunnableLambda(print_prompt) | self.model | StrOutputParser()

    def retriever_doc(self, query: str) -> list[Document]:
        """ 检索用户查询相关的文档 """
        docs = self.retriever.invoke(input=query)
        return docs

    def rag_summarize(self, query: str) -> str:

        # 先检索文档，再把文档和用户查询一起传入模型，最后返回

        docs = self.retriever_doc(query)
        context = "; ".join([ doc.page_content for doc in docs])

        input = {
            "input": query,
            "context": context,
        }

        resp = self.chain.invoke(input)

        return resp


rag = RagService()

if __name__ == '__main__':

    rag = RagService()

    query = "怎么使用拖地功能"
    query = "小户型适合哪种扫地机器人"
    # docs = rag.retriever_doc(query)
    # print(len(docs))
    # print(docs)

    print()

    res = rag.rag_summarize(query)

    print(res)

    pass