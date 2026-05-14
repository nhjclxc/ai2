#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/5 15:33
# Module    : langchian07_chains链的基本使用.py
# explain   :
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_core.runnables import RunnableLambda, RunnableSerializable

from langchain02_heima.lc00_core.model_helper import get_chat_openai

"""

chain链的作用：可以将组件串联，将上一个组件的输出作为下一个组件的输入
核心前提：组件必须实现了 langchain_core.runnables.base.Runnable 类

chain = prompt_template | model

左边 prompt_template 的输出，可以直接作为右边 model 的输入使用

"""

def chain_example1():

    chat_template = ChatPromptTemplate.from_messages([
        ('system', "你是一个精通化学式的助手，我会给你中文名字，你给我返回对应的化学式。"),
        MessagesPlaceholder(variable_name="historys"),
        ('human', "根据以上示例回答以下问题，问题：{input_question}")
    ])

    historys = [
        ('human', "水"),
        ('ai', "H₂o"),
        ('human', "氧气"),
        ('ai', "O₂"),
        ('human', "硫酸"),
        ('ai', "H₂So₄"),
    ]

    chat = get_chat_openai(streaming=True)

    # 使用 RunnableLambda(prompt_debug) 来输出 chat_template 构造出来的提示词
    # 将 RunnableLambda(prompt_debug) 构造为一个chain链的组件
    # 那么 RunnableLambda(prompt_debug) 的输入接收的为 上一个组件chat_template 的输出，输出的送给 chat作为输入
    chain: RunnableSerializable = chat_template | RunnableLambda(prompt_debug) | chat

    input_question = "草酸钙、碳酸钙、高锰酸钾"
    resp = chain.stream(input={"historys": historys, "input_question": input_question})
    for chunk in resp:
        # chunk 的类型 langchain_core.messages.ai.AIMessageChunk
        print(chunk.content, end="", flush=True)


def prompt_debug(x: PromptValue) -> PromptValue:
    print("=========== 构造的提示词 ===========")
    print(x.to_string())
    print("=========== 构造的提示词 ===========")
    return x


# chain_example1()

# from typing import Self
# | 或 __or__ 运算符重载
class MyOrClass:
    def __init__(self, data):
        self.data = data

    # 重载  | 或运算符
    def __or__(self, other) -> 'MyOrClass':
        # self 是 | 前面的对象，即当前调用对象
        # other 是 | 后面的对象，即要被或的目标对象
        print(f"__or__: {other}")
        return MyOrClass(f"{self.data} -> {other}")
    def __str__(self):
        return self.data
    def run(self):
        return self.data

or1 = MyOrClass("a")
or2 = MyOrClass("b")

print(or1)
print(or2)
or12 = or1 | or2
or21 = or2.__or__(or1)
print(or12)
print(or21)

or1221 = or12 | or21

print(or1221)
print(or1221.run())


# Runnable 接口






