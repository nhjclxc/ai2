#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/12 21:46
# Module    : agent01.py
# explain   : agent初体验
import random

from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool

from langchain02_heima.lc00_core.model_helper import get_chat_openai

fujian_cities = [
    "福州", "厦门", "泉州", "漳州", "莆田", "三明", "南平", "龙岩", "宁德"
]
taiwan_cities = [
    "台北", "新北", "桃园", "台中", "台南", "高雄", "基隆", "新竹", "嘉义"
]
weather_types1 = [
    "小雨", "大雨", "小雪", "中雪",
]
weather_types2 = [
    "中雨", "暴雨", "大雪", "暴雪"
]

@tool(description="天气查询")
def searchh_weather(city) -> str:

    # 注意单纯的 agent 还无法实现工具调用之间的参数传递，要想实现参数传递，必须使用 LangGraph

    if city in fujian_cities:
        weather_types = weather_types1
    elif city in taiwan_cities:
        weather_types = weather_types2
    else:
        weather_types = weather_types1 + weather_types2

    res = random.choice(weather_types)

    print(f"searchh_weather 工具被调用 res = {res}")

    return res


@tool(description="获取城市")
def location() -> str:
    cities = fujian_cities + taiwan_cities

    res = random.choice(cities)

    print("location 工具被调用，", res)

    return res


# 在langchain 中创建一个 agent
agent = create_agent(
    model=get_chat_openai(streaming=True),
    tools=[searchh_weather, location],
    system_prompt="你是一个聊天助手，可以回答用户提出的问题，不要由过多的废话，只要回答用户问题即可"
)

other = "如果天气带雨则提醒我带伞，如果天气有雪则叫我穿衣服，其他则表示好天气开开心心出门"
other += "; 如果是福建省的城市则说在大陆，如果是台湾的城市则说在台湾"
content = f"根据已知的searchh_weather和location工具，调用他们返回当前城市和对应的天气，{other}"

def test_invoke():
    resp = agent.invoke(
        input={
            "messages": [
                {"role": "user", "content": content}
            ]
        }
    )
    # print(resp)
    # {'messages': [HumanMessage(content='根据已知的searchh_weather和location工具，调用他们返回当前城市和对应的天气', additional_kwargs={}, response_metadata={}, id='2264497c-cfe1-4c3d-aa12-91f05efc7602'), AIMessage(content='', additional_kwargs={}, response_metadata={'finish_reason': 'tool_calls', 'model_name': 'qwen-plus', 'model_provider': 'openai'}, id='lc_run--019e1c92-4a77-7002-a534-7652019a55f5', tool_calls=[{'name': 'location', 'args': {}, 'id': 'call_3a28b71fe0164165be1976', 'type': 'tool_call'}, {'name': 'searchh_weather', 'args': {}, 'id': 'call_1becb902b52442d39a6ac6', 'type': 'tool_call'}], invalid_tool_calls=[]), ToolMessage(content='三明', name='location', id='f3e4bc41-8558-442a-89f5-9e816caefc3a', tool_call_id='call_3a28b71fe0164165be1976'), ToolMessage(content='["多云"]', name='searchh_weather', id='184ecde2-bee5-4f77-8311-1907b32813c9', tool_call_id='call_1becb902b52442d39a6ac6'), AIMessage(content='当前城市是三明，天气为多云。', additional_kwargs={}, response_metadata={'finish_reason': 'stop', 'model_name': 'qwen-plus', 'model_provider': 'openai'}, id='lc_run--019e1c92-5191-7fd0-9713-b98d8a3cc6d2', tool_calls=[], invalid_tool_calls=[])]}

    parser = StrOutputParser()

    for res in resp["messages"]:
        print(f"{type(res).__name__}: {parser.invoke(res)}")

# test_invoke()

def test_stream():
    resps = agent.stream(
        input={
            "messages": [
                {"role": "user", "content": content}
            ]
        },
    )

    for resp in resps:
        # print(resp)
        role = None
        if 'tools' in resp:
            # {'tools': {'messages': [ToolMessage(content='台北', name='location', id='e6fb2a27-e9c3-4ab3-ae61-49c6cf37f4c9', tool_call_id='call_b3b6c276d77144908fe351')]}}
            # print('tools ', resp.get("tools").get("messages"))
            for msg in resp.get("tools").get("messages"):
                print(f"【{type(msg).__name__} -> {msg.name}：】{msg.content}")
        if 'model' in resp:
            # {'model': {'messages': [AIMessage(content='当前城市是台北，天气为霜冻。', additional_kwargs={},response_metadata={'finish_reason': 'stop', 'model_name': 'qwen-plus','model_provider': 'openai'},id='lc_run--019e1c93-bec0-7091-bf8d-c7c865725771', tool_calls=[],invalid_tool_calls=[])]}}
            # print('model ', resp.get("model").get("messages"))
            for msg in resp.get("model").get("messages"):
                # llm要求调用工具时返回的内容如下：
                # 【model：】content='' additional_kwargs={} response_metadata={'finish_reason': 'tool_calls', 'model_name': 'qwen-plus', 'model_provider': 'openai'} id='lc_run--019e2157-9adc-7902-a98d-b1f03628fed6' tool_calls=[{'name': 'location', 'args': {}, 'id': 'call_9c04e03ba98b4b23921a4b', 'type': 'tool_call'}, {'name': 'searchh_weather', 'args': {}, 'id': 'call_552a2eeee8ad47b3b58261', 'type': 'tool_call'}] invalid_tool_calls=[]
                if msg.response_metadata.get('finish_reason') == "tool_calls":
                    # print('要调用的工具列表， ', msg.tool_calls)
                    tool_calls_list = []
                    for tool in msg.tool_calls:
                        tool_calls_list.append(f"工具：{tool.get('name')}, 参数：{tool.get('args')}")
                    tool_calls_str = "; ".join(tool_calls_list)
                    print(f"【{type(msg).__name__} 工具调用：】{tool_calls_str}")
                else:
                    # llm正常回复消息时，返回的内容如下：
                    # content='当前城市是漳州，天气是晴天，好天气开开心心出门；漳州在大陆。' additional_kwargs={} response_metadata={'finish_reason': 'stop', 'model_name': 'qwen-plus', 'model_provider': 'openai'} id='lc_run--019e2157-a0de-72b0-ba3b-799312114ae4' tool_calls=[] invalid_tool_calls=[]
                    print(f"【{type(msg).__name__}：】{msg.content}")

# test_stream()

def test_stream_values():

    resps = agent.stream(
        input={
            "messages": [
                {"role": "user", "content": content}
            ]
        },
        stream_mode="values"
    )
    # print(resps)

    for resp in resps:

        # print(resp)
        # {'messages': [HumanMessage(content='根据已知的searchh_weather和location工具，调用他们返回当前城市和对应的天气，如果天气带雨则提醒我带伞，如果天气有雪则叫我穿衣服，其他则表示好天气开开心心出门; 如果是福建省的城市则说在大陆，如果是台湾的城市则说在台湾', additional_kwargs={}, response_metadata={}, id='4a80dfa3-ed70-42d4-8868-8766f1ac6c49'), AIMessage(content='', additional_kwargs={}, response_metadata={'finish_reason': 'tool_calls', 'model_name': 'qwen-plus', 'model_provider': 'openai'}, id='lc_run--019e2164-f09d-78e0-a9eb-18716411f0f0', tool_calls=[{'name': 'location', 'args': {}, 'id': 'call_7ed042c7d49e417689d11c', 'type': 'tool_call'}, {'name': 'searchh_weather', 'args': {}, 'id': 'call_d428027bc0434418b9987e', 'type': 'tool_call'}], invalid_tool_calls=[]), ToolMessage(content='三明', name='location', id='de816ce9-68e8-457f-bdf9-b55fc208c9e9', tool_call_id='call_7ed042c7d49e417689d11c'), ToolMessage(content='大雪', name='searchh_weather', id='a43397f6-a93d-4680-81d1-be97989655eb', tool_call_id='call_d428027bc0434418b9987e'), AIMessage(content='在大陆，天气有雪，叫我穿衣服', additional_kwargs={}, response_metadata={'finish_reason': 'stop', 'model_name': 'qwen-plus', 'model_provider': 'openai'}, id='lc_run--019e2164-f5e3-76b2-85d9-e60d621f759e', tool_calls=[], invalid_tool_calls=[])]}

        # 每一次都会将前面的消息带回来？？？
        # 为什么要带回来？
        # 那么我们不需要遍历整个消息了，只需要解析最后一个消息即可
        # for msg in resp.get("messages"):

        # 表示每一次都取最后一个消息，即最新的消息，拿出来解析，前面的就不理他了
        msg = resp.get("messages")[-1]
        if type(msg).__name__ == "AIMessage" and msg.response_metadata.get("finish_reason") == "tool_calls":

            tool_calls_list = []
            for tool in msg.tool_calls:
                tool_calls_list.append(f"工具：{tool.get('name')}, 参数：{tool.get('args')}")
            tool_calls_str = "; ".join(tool_calls_list)

            print(f"{type(msg).__name__} 工具调用: {tool_calls_str}")

        else:
            print(f"{type(msg).__name__}: {msg.content}")


            pass



    pass

test_stream_values()


# if __name__ == '__main__':
#     print(searchh_weather())
