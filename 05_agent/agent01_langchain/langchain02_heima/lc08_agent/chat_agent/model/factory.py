#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/16 21:27
# Module    : factory.py
# explain   : 模型生成器工厂

import os
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional

from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


load_dotenv(Path(__file__).parent.parent.parent.parent.with_name(".env"))
openai_api_key = os.getenv("OPENAI_API_KEY")
qwen_api_key = os.getenv("QWEN_API_KEY")
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
model_chat = "qwen3.6-plus"
model_embed = "text-embedding-v4"

HTTPS_PROXY = os.getenv("HTTPS_PROXY")
if HTTPS_PROXY:
    os.environ["HTTPS_PROXY"] = HTTPS_PROXY

class ModelFactory(ABC):
    @abstractmethod
    def gen_model(self) -> Optional[Embeddings | BaseChatModel]:
        pass

class ChatModelFactory(ModelFactory):
    def gen_model(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatOpenAI(
            model=model_chat,
            streaming=True,
            base_url=base_url,
            api_key=qwen_api_key,
        )

class EmbeddinglFactory(ModelFactory):
    def gen_model(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(
            model=model_embed,
            dashscope_api_key=qwen_api_key
        )

chat_model = ChatModelFactory().gen_model()

embed_model = EmbeddinglFactory().gen_model()

if __name__ == '__main__':

    resp = chat_model.stream(input="hello")
    for r in resp:
        print(r.content, end="", flush=True)

    print("="*60)

    res = embed_model.embed_query("hello")
    print(len(res))


    pass