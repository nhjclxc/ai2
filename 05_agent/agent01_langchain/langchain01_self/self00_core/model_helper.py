#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/29 21:37
# Module    : model_helper.py
# explain   : 在这个文件里面，创建llm或者chat客户端

import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.embeddings import Embeddings
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import DashScopeEmbeddings

load_dotenv(Path(__file__).parent.parent.with_name(".env"))
openai_api_key = os.getenv("OPENAI_API_KEY")
qwen_api_key = os.getenv("QWEN_API_KEY")
qwen_base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
qwen_model_chat = "qwen3.6-plus"

HTTPS_PROXY = os.getenv("HTTPS_PROXY")
if HTTPS_PROXY:
    os.environ["HTTPS_PROXY"] = HTTPS_PROXY
# v2RayN
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:10808"
# clash
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

# codex resume 019e258a-a611-76b3-b641-f5d9e7898ad0

def get_llm_openai(base_url=qwen_base_url, api_key=qwen_api_key) -> OpenAI:
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

def get_chat_openai(model=qwen_model_chat, temperature=0.7, base_url=qwen_base_url, api_key=qwen_api_key,
            streaming: bool = False, callbacks: list[BaseCallbackHandler]=None) -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        base_url=base_url,
        api_key=api_key,
        streaming=streaming,
        callbacks=callbacks
    )

# 创建@langchain01_self/self01_llm/Self-Study-Langchain-LLM-Map.md文件，详细给出学习Langchain的llm的学习路线

# model_embed = "text-embedding-v3"
model_embed = "text-embedding-v4"

def get_embedding_model(model=model_embed, api_key=qwen_api_key) -> Embeddings:
    return DashScopeEmbeddings(
    model=model,
    dashscope_api_key=api_key
)



if __name__ == "__main__":

    chat = get_chat_openai(streaming=True)
    resp = chat.stream(input="who are you?")

    for res in resp:
        print(res.content, end="", flush=True)
