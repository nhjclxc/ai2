#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/13 22:04
# Module    : agent03_middleware中间件.py
# explain   :

# langchain 默认支持的 中间件 https://docs.langchain.com/oss/python/langchain/middleware/built-in

"""
1. agent执行前
2. agent执行后
3. model执行前
4. model执行后
5. 工具执行中
6. 模型执行中
"""
from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import before_agent, after_agent, after_model, before_model, wrap_tool_call, \
    wrap_model_call
from langchain_core.tools import tool
from langgraph.runtime import Runtime

from langchain02_heima.lc00_core.model_helper import get_chat_openai


@tool(description="获取指定城市的天气数据，传入城市名称，返回该城市今天的天气数据")
def get_weather(city: str) -> str:
    return f" 城市 {city} 的天气是晴天。"

@before_agent
def before_agent_log(state: AgentState, runtime: Runtime) -> None:
    print("【【【before_agent】】】", f"消息数量：{len(state["messages"])}")

@after_agent
def after_agent_log(state: AgentState, runtime: Runtime) -> None:
    print("【【【before_agent】】】", f"消息数量：{len(state["messages"])}")

@before_model
def before_model_log(state: AgentState, runtime: Runtime) -> None:
    print("【【【before_model_log】】】", f"消息数量：{len(state["messages"])}")

@after_model
def after_model_log(state: AgentState, runtime: Runtime) -> None:
    print("【【【after_model_log】】】", f"消息数量：{len(state["messages"])}")

# 工具执行中
@wrap_tool_call
def wrap_tool_call_log(request, handler):
    print("【【【wrap_tool_call_log】】】", f"工具调用参数：{request.tool_call["args"]}")
    return handler(request)

# 模型执行中
@wrap_model_call
def wrap_model_call_log(request, handler):
    print("【【【wrap_model_call_log】】】")
    return handler(request)

agent = create_agent(
    model=get_chat_openai(streaming=True),
    tools=[get_weather],
    middleware=[before_agent_log, after_agent_log, before_model_log, after_model_log, wrap_tool_call_log, wrap_model_call_log],
)

resp = agent.stream(
    input={"messages": [{'role': "user", 'content': "今天厦门的天气怎么样？"}]},
    stream_mode="values"
)

for r in resp:
    msg = r["messages"][-1]
    print(msg)

#
# from langchain.agents import create_agent, AgentState
# from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, \
#     wrap_tool_call
# from langchain_community.chat_models.tongyi import ChatTongyi
# from langchain_core.tools import tool
# from langgraph.runtime import Runtime
#
#
# @tool(description="查询天气，传入城市名称字符串，返回字符串天气信息")
# def get_weather(city: str) -> str:
#     return f"{city}天气：晴天"
#
#
#
#
# @before_agent
# def log_before_agent(state: AgentState, runtime: Runtime) -> None:
#     # agent执行前会调用这个函数并传入state和runtime两个对象
#     print(f"[before agent]agent启动，并附带{len(state['messages'])}消息")
#
#
# @after_agent
# def log_after_agent(state: AgentState, runtime: Runtime) -> None:
#     print(f"[after agent]agent结束，并附带{len(state['messages'])}消息")
#
#
# @before_model
# def log_before_model(state: AgentState, runtime: Runtime) -> None:
#     print(f"[before_model]模型即将调用，并附带{len(state['messages'])}消息")
#
#
# @after_model
# def log_after_model(state: AgentState, runtime: Runtime) -> None:
#     print(f"[after_model]模型调用结束，并附带{len(state['messages'])}消息")
#
#
# @wrap_model_call
# def model_call_hook(request, handler):
#     print("模型调用啦")
#     return handler(request)
#
#
# @wrap_tool_call
# def monitor_tool(request, handler):
#     print(f"工具执行：{request.tool_call['name']}")
#     print(f"工具执行传入参数：{request.tool_call['args']}")
#
#     return handler(request)
#
#
# agent = create_agent(
#     model=ChatTongyi(model="qwen3-max"),
#     tools=[get_weather],
#     middleware=[log_before_agent, log_after_agent, log_before_model, log_after_model, model_call_hook, monitor_tool]
# )
#
# res = agent.invoke({"messages": [{"role": "user", "content": "深圳今天的天气如何呀，如何穿衣"}]})
# print("**********\n", res)
