#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/28 19:31
# Module    : langchain01_调用大模型.py
# explain   :


import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage,SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv(Path(__file__).parent.with_name(".env"))
openai_api_key = os.getenv("OPENAI_API_KEY")
qwen_api_key = os.getenv("QWEN_API_KEY")
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
model = "qwen-plus"
# model = "gpt-4o-mini" # 或 gpt-4o / gpt-4.1

def get_llm_openai(model=model, temperature=0.7, base_url=base_url, api_key=qwen_api_key,
            streaming: bool = False, callbacks: list[BaseCallbackHandler]=None) -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        base_url=base_url,
        api_key=api_key,
        streaming=streaming,
        callbacks=callbacks
    )

def stream_base():

    llm = get_llm_openai(streaming = True)

    response = llm.stream("帮我写一首情歌")

    for chunk in response:
        print(chunk.content, end="", flush=True)

# stream_base()

# 流式输出的回调函数
class MyHandlerStream(BaseCallbackHandler):
    def on_llm_new_token(
        self,
        token: str,
        **kwargs,
    ) -> Any:

        print(token, end="", flush=True)

def stream_handler():
    # 流式输出支持回调函数

    llm = get_llm_openai(streaming = True, callbacks=[MyHandlerStream()])

    llm.invoke("给出《Attention is all you nedd》论文的摘要")
    # 在创建 llm 的时候注册了回调处理函数的话，就可以不需要获取invoke的返回值了

# stream_handler()

def llm_messages_stream():
    llm = get_llm_openai(streaming = True)

    messages = [
        SystemMessage("你是一个中文听力考试助手，注意在回答问题的时候只要给答案即可，无须给出过多无用内容"),
        HumanMessage("听力题目：今天天气很好，我早上八点起床，吃完早饭，准备去公园散步。"),
        HumanMessage("根据上述历史消息记录，回答以下问题：1、今天天气怎么样？2、我几点起床？3、我吃完早饭要去哪里？注意给出最终答案既可以，不要加其他与答案无关的文字"),
    ]

    response = llm.stream(messages)

    for chunk in response:
        print(chunk.content, end="", flush=True)

# llm_messages_stream()


def llm_messages_prompt_stream():

    llm = get_llm_openai(streaming = True)

    prompt = ChatPromptTemplate.from_messages([
        ('system', "你是一个中文听力考试助手，注意在回答问题的时候只要给答案即可，无须给出过多无用内容"),
        ('human', '听力题目：今天天气很好，我早上八点起床，吃完早饭，准备去公园散步。'),
        ('human', '问题: {question}')
    ])

    chain = prompt | llm

    res = chain.stream({"question": "1、今天天气怎么样？2、我几点起床？3、我吃完早饭要去哪里？"})

    for chunk in res:
        print(chunk.content, end="", flush=True)

# llm_messages_prompt_stream()

def llm_messages_dynamic_stream():

    llm = get_llm_openai(streaming = True)

    prompt = ChatPromptTemplate.from_messages([
        ('system', "你是一个中文听力考试助手，注意在回答问题的时候只要给答案即可，无须给出过多无用内容"),
        MessagesPlaceholder(variable_name="history"),
        ('human', '问题: {question}')
    ])

    messages = [
        HumanMessage(content="听力题目：今天天气很好，我早上八点起床，吃完早饭，准备去公园散步。")
    ]

    chain = prompt | llm

    response = chain.stream({
        "history": messages,
        "question": "1、今天天气怎么样？2、我几点起床？3、我吃完早饭要去哪里？"
    })

    for chunk in response:
        print(chunk.content, end="", flush=True)

# llm_messages_dynamic_stream()


def tongyi_test1_stream():

    from langchain_community.llms.tongyi import Tongyi
    llm = Tongyi(
        model="qwen-plus",
        api_key=qwen_api_key,
        streaming=True
    )

    res = llm.stream("截止2020年1约1号，世界上有多少个国家")

    for chunk in res:
        print(chunk, end="", flush=True)


tongyi_test1_stream()

