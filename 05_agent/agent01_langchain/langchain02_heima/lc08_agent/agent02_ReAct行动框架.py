#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/13 21:24
# Module    : agent02_ReAct行动框架.py
# explain   :
import random

from langchain.agents import create_agent
from langchain_core.tools import tool

from langchain02_heima.lc00_core.model_helper import get_chat_openai


# 使用 langchain 的 agent 已经实现了 react 框架
# react -> re 表示重复（不断地） act -> action 表示动作行为（即表示llm需要取调用哪些工具）


@tool(description="获取身高，单位cm")
def get_height() -> int:
    height = random.randint(150, 190)
    # print(f"LLM调用获取 身高 工具，返回值：{height}")
    return height

@tool(description="获取体重，单位kg")
def get_weight() -> int:
    weight = random.randint(50, 90)
    # print(f"LLM调用获取 体重 工具，返回值：{weight}")
    return weight


agent = create_agent(
    model=get_chat_openai(streaming=True),
    tools=[get_weight, get_height],
    system_prompt="""你是一个严格执行ReAct框架的智能体，必须按照【思考 -> 行动 -> 观察 -> 再思考】的流程解决问题。
    并且每一轮的思考只能调用一个工具，禁止一次思考调用多个工具，并告知我你的思考过程，工具调用的原因，按照思考、观察、行动三个结构告诉我"""
)

resp = agent.stream(
    input={"messages":[{'role': 'user', 'content': "请计算我的BMI值"}]},
    stream_mode="values"
)

for res in resp:

    msg = res['messages'][-1]
    if type(msg).__name__ == "HumanMessage":
        print(f"{type(msg).__name__} -->>> {msg.content}")
    elif type(msg).__name__ == "AIMessage":
        tool_calls_str = ""
        if msg.response_metadata.get("finish_reason") == "tool_calls":
            tool_calls_list = []
            for tool in msg.tool_calls:
                tool_calls_list.append(f"工具名称：{tool.get('name')}， 参数：{tool.get('args')}")
            tool_calls_str = " -> ".join(tool_calls_list)
        # print(f"{type(msg).__name__} -->>> {msg.content}, 工具调用内容：{tool_calls_str}")
        print(f"{type(msg).__name__} -->>> {msg.content}")
    elif type(msg).__name__ == "ToolMessage":
        print(f"{type(msg).__name__} -->>> 调用工具 {msg.name} , 返回数据：{msg.content}")


    pass
