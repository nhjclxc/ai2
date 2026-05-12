#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/28 19:31
# Module    : langchain01_调用大模型.py
# explain   :


import os
from pathlib import Path
from dotenv import load_dotenv
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

def get_llm(model=model, temperature=0.7, base_url=base_url, api_key=qwen_api_key) -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        base_url=base_url,
        api_key=api_key
    )

def llm_base():
    # 第一步：创建大模型对象
    llm = ChatOpenAI(
        model=model,
        temperature=0.7,
        base_url=base_url,
        api_key=qwen_api_key
    )
    # 输入提示词调用大模型
    response = llm.invoke("你是什么模型?")
    # llm返回数据解析
    print(response.content)

# llm_base()


def llm_simple_chain():
    """ 带有 prompts 的调用 """

    # 得到一个llm对象
    llm = get_llm()

    # 构建提示词模板
    prompts = ChatPromptTemplate.from_template("请把这句话翻译成英语：{text}")

    # 设置一个调用链
    # 先处理 prompts 接着将 prompts处理的输出结果传给 llm
    chain = prompts | llm

    # response = chain.invoke({"text": "Where are you from?"})
    response = chain.invoke({"text": "我可以帮你把一整套 LangChain + OpenAI + Agent（工具调用）最小可运行模板搭出来，避免你后面继续踩坑。"})

    print(response.content)

# llm_simple_chain()

def llm_messages():
    """ 带有历史消息的大模型调用 """

    llm = get_llm()

    messages = [
        SystemMessage("下面你将作为一个中文听力考试的考试，我将给你文本题目，要求你根据文本题目和我的问题得到答案。"),
        HumanMessage("听力题目：今天天气很好，我早上八点起床，吃完早饭，准备去公园散步。"),
        HumanMessage("根据上述历史消息记录，回答以下问题：1、今天天气怎么样？2、我几点起床？3、我吃完早饭要去哪里？注意给出最终答案既可以，不要加其他与答案无关的文字"),
    ]

    response = llm.invoke(messages)
    print(response)
    print(response.content)

    pass

# llm_messages()

def llm_messages_prompt():

    llm = get_llm()

    # 注意 多个消息要使用 from_messages
    # 注意 当个消息使用 from_template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "下面你将作为一个中文听力考试的考试，我将给你文本题目，要求你根据文本题目和我的问题得到答案。"),
        ("human", "听力题目：今天天气很好，我早上八点起床，吃完早饭，准备去公园散步。"),
        ("human", "问题：{question}")
    ])

    chain = prompt | llm

    response = chain.invoke({"question": "几点起床，起床后去哪里？"})

    print(response.content)

# llm_messages_prompt()

def llm_messages_dynamic():
    # 支持messages 的动态拼接

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "现在你是一个中文考试助手。注意给出最终答案既可以，不要加其他与答案无关的文字"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "问题：{question}")
    ])

    messages = [
        HumanMessage(content="听力题目：今天天气很好，我早上八点起床，吃完早饭，准备去公园散步。")
    ]

    chain = prompt | llm

    response = chain.invoke({
        "history": messages,
        "question": "1、几点起床。2、起床后去哪里（位置）？"
    })

    print(response.content)

# llm_messages_dynamic()


# 基于 langchain 来使用tongyi 的llm
from langchain_community.llms.tongyi import Tongyi

def tongyi_test1():

    llm = Tongyi(
        model="qwen-plus",
        api_key=qwen_api_key,
    )

    response = llm.invoke("你是哪一个的大模型？model版本号是多少？训练时间是什么时候")

    print(response)

tongyi_test1()
