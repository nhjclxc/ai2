#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/26 14:33
# Module    : main.py
# explain   :


import os
from collections.abc import Iterable
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from openai.lib.streaming.chat import ChunkEvent
from openai.types.chat import ChatCompletionMessageParam

# 加载环境变量
load_dotenv(Path(__file__).parent / "../.env")

qwen_api_key = os.getenv("QWEN_API_KEY")
print(f"qwen_api_key: {qwen_api_key}")

# 调用千问的语言模型
# https://bailian.console.aliyun.com/cn-beijing/?tab=api#/api/?type=model&url=3016807


# 大陆
# SDK 调用配置的base_url：https://dashscope.aliyuncs.com/compatible-mode/v1
# HTTP 请求地址：POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

# 海外
# SDK 调用配置的base_url：https://dashscope-us.aliyuncs.com/compatible-mode/v1
# HTTP 请求地址：POST https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions
# base_url = "https://dashscope-us.aliyuncs.com/compatible-mode/v1"
# url = "https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions"

# os.environ["HTTP_PROXY"] = "http://127.0.0.1:10808"
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:10808"


# 千问支持的模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models

# 在下面这个链接里面开通你所需要的免费版模型
# https://bailian.console.aliyun.com/cn-beijing/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.6e57133cOOTXIA&tab=model#/model-usage
model = "qvq-max-2025-03-25"
model = "qwen-plus"



# 如何调用模型，注意看官网给出的示例代码
# https://bailian.console.aliyun.com/cn-beijing/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.6e57133cOOTXIA&tab=api#/api/?type=model&url=3016807


# 创建openai客户端
client = OpenAI(
    api_key=qwen_api_key,
    base_url=base_url,
)

msgs = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？什么模型？"}
]

# 调用对话
def chat():

    response = client.chat.completions.create(
        model=model,
        messages=msgs,
    )
    # {"id":"chatcmpl-b4399a33-0a1f-9068-bef0-4ed1029b6859","choices":[{"finish_reason":"stop","index":0,"logprobs":null,"message":{"content":"你好！我是通义千问（Qwen），是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，甚至玩游戏。\n\n我支持多种语言，包括但不限于中文、英文、法语、西班牙语、葡萄牙语、俄语、阿拉伯语、日语、韩语、越南语、泰语、印尼语等。\n\n如果你有任何问题或需要帮助，欢迎随时告诉我！😊","refusal":null,"role":"assistant","annotations":null,"audio":null,"function_call":null,"tool_calls":null}}],"created":1777186635,"model":"qwen-plus","object":"chat.completion","service_tier":null,"system_fingerprint":null,"usage":{"completion_tokens":114,"prompt_tokens":25,"total_tokens":139,"completion_tokens_details":null,"prompt_tokens_details":{"audio_tokens":null,"cached_tokens":0}}}
    print(response.model_dump_json())

# chat()

def chat_stream():
    # https://bailian.console.aliyun.com/cn-beijing/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.6e57133cOOTXIA&tab=doc#/doc/?type=model&url=2866129

    response = client.chat.completions.create(
        model=model,
        messages=msgs,
        stream=True
    )
    for chunk in response:
        print(chunk.choices[0].delta.content, end="", flush=True)
        # print(chunk.model_dump_json())
        pass

    pass


# chat_stream()

# system
# assistant
# user

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage# 得到模型对象，qwen3-max就是聊天模型
def chat_stream2():

    # response = client.chat.completions.create(
    #     model=model,
    #     messages= [
    #         {"role": "system", "content": "你是我的AI助理，回答问题很简洁"},
    #         {"role": "user", "content": "现在有一个也鸡兔同笼问题：鸡兔共有头10个，腿30个，求鸡和兔的数量？"},
    #         {"role": "assistant", "content": "答：鸡 5 只，兔 5 只。"},
    #         {"role": "user", "content": "现在又抓来鸡兔若干只，不知道有多少个头，但是知道新增16只脚，请问新增的鸡兔数量有多少种可能？鸡兔分别可能增加的数量是多少，笼里总共有鸡兔的可能是哪些？"},
    #     ],
    #     stream=True
    # )
    # for chunk in response:
    #     print(chunk.choices[0].delta.content, end="", flush=True)
    #     # print(chunk.model_dump_json())
    #     pass

    with client.chat.completions.stream(
            model=model,
            messages=[
                {"role": "system", "content": "你是我的AI助理，回答问题很简洁"},
                {"role": "user", "content": "现在有一个鸡兔同笼问题：鸡兔共有头10个，腿30个，求鸡和兔的数量？"},
                {"role": "assistant", "content": "答：鸡 5 只，兔 5 只。"},
                {"role": "user",
                 "content": "现在又抓来鸡兔若干只，不知道有多少个头，但是知道新增16只脚，请问新增的鸡兔数量有多少种可能？鸡兔分别可能增加的数量是多少，笼里总共有鸡兔的可能是哪些？"},
            ],
    ) as stream:
        for event in stream:
            # if hasattr(event, "chunk"):
            #     chunk = event.chunk
            #     if hasattr(chunk, "choices"):
            #         delta = chunk.choices[0].delta
            #         print(delta.content, end="", flush=True)

            chunk = getattr(event, "chunk", None)
            if not chunk or not hasattr(chunk, "choices"):
                continue

            delta = chunk.choices[0].delta
            content = getattr(delta, "content", None)

            if content:
                print(content, end="", flush=True)

def extract_content(event):
    chunk = getattr(event, "chunk", None)
    if not chunk:
        return None

    if not hasattr(chunk, "choices"):
        return None

    delta = chunk.choices[0].delta
    return getattr(delta, "content", None)
def stream_parser(stream):
    for event in stream:
        chunk = getattr(event, "chunk", None)
        if not chunk:
            continue

        if not hasattr(chunk, "choices"):
            continue

        delta = chunk.choices[0].delta
        content = getattr(delta, "content", None)

        if content:
            yield content

chat_stream2()
