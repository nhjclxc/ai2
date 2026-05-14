#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/29 19:44
# Module    : langchain03_聊天模型.py
# explain   :

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv(Path(__file__).parent.with_name(".env"))
openai_api_key = os.getenv("OPENAI_API_KEY")
qwen_api_key = os.getenv("QWEN_API_KEY")
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
model = "qwen-plus"


# SystemMessage, system
# HumanMessage，user
# AIMessage，assistant

# 聊天模型使用 chat_models 包下面的聊天模型，不再是 llms 包下的了
# from langchain_community.chat_models.openai import ChatOpenAI

def get_chat_openai(model=model, temperature=0.7, base_url=base_url, api_key=qwen_api_key,
            streaming: bool = False, callbacks: list[BaseCallbackHandler]=None) -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        base_url=base_url,
        api_key=api_key,
        streaming=streaming,
        callbacks=callbacks
    )

def chat_base():
    # 基础聊天模型

    chat = get_chat_openai(streaming=True)

    messages = [
        SystemMessage(content="你是一个精通唐诗三百首的诗歌助手，我会给你部分的诗句，你要给我得到他是哪一首诗歌，并且给出作者，只要给出诗歌名称和作者即可，不要有废话"),
        HumanMessage("第一个诗歌：举头望明月，低头思故乡；第二个诗歌：春眠不觉晓，处处闻啼鸟；第三个诗歌：白日依山尽，黄河入海流")
    ]

    messages = [
        SystemMessage(content="你是一个精通唐诗三百首的诗歌助手，我会给你部分的诗句，要求你回答剩余部分，只要给出诗歌剩余部分即可，不要有废话"),
        HumanMessage("第一个诗歌：举头望明月，低头思故乡；第二个诗歌：春眠不觉晓，处处闻啼鸟；第三个诗歌：白日依山尽，黄河入海流")
    ]

    res = chat.stream(messages)

    for chunk in res:
        print(chunk.content, end="", flush=True)

    pass

# chat_base()


def chat_simple():

    chat = get_chat_openai(streaming=True)

    # 不在使用类对象来标识消息类型，而是使用元组来标识，一个元组有两个元素 ('role', 'message')，第一个是角色，第二个是消息。如：('human', '你是谁？')
    # system，human，ai
    messages = [
        ('system', "你是一个精通唐诗三百首的诗歌助手，我会给你部分的诗句，要求你回答剩余部分，只要给出诗歌剩余部分即可，不要有废话"),
        ('human', "第一个诗歌：举头望明月，低头思故乡；第二个诗歌：春眠不觉晓，处处闻啼鸟；第三个诗歌：白日依山尽，黄河入海流")
    ]

    # 类对象和简写形式的重要区别是，简写形式支持消息的变量注入
    # "我的名字是: {name}"

    res = chat.stream(messages)

    for chunk in res:
        print(chunk.content, end="", flush=True)

# chat_simple()

def chat_simple_var():
    # 消息支持变量

    chat = get_chat_openai(streaming=True)

    prompt = ChatPromptTemplate.from_messages([
        ('system', "你是一个精通唐诗三百首的诗歌助手，我会给你部分的诗句，要求你回答剩余部分，只要给出诗歌剩余部分即可，不要有废话"),
        # MessagesPlaceholder(variable_name="history"),
        ('human', "第一个诗歌：举头望明月，低头思故乡；第二个诗歌：{something}；第三个诗歌：白日依山尽，黄河入海流")
    ])

    chain = prompt | chat

    res = chain.stream({
        "something": "春眠不觉晓，处处闻啼鸟"
    })

    for chunk in res:
        print(chunk.content, end="", flush=True)


chat_simple_var()


