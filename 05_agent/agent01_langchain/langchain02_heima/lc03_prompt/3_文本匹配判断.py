#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/26 20:38
# Module    : 3_文本匹配判断.py
# explain   :

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv(Path(__file__).parent / "../.env")

qwen_api_key = os.getenv("QWEN_API_KEY")
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
model = "qwen-plus"
print(f"qwen_api_key: {qwen_api_key}")
print(f"base_url: {base_url}")
print(f"model: {model}")

client = OpenAI(
    api_key=qwen_api_key,
    base_url=base_url
)


examples_data = {
    "是": [
        ("公司ABC发布了季度财报，显示盈利增长。", "财报披露，公司ABC利润上升。"),
        ("公司ITCAST发布了年度财报，显示盈利大幅度增长。", "财报披露，公司ITCAST更赚钱了。")
    ],
    "不是": [
        ("黄金价格下跌，投资者抛售。", "外汇市场交易额创下新高。"),
        ("央行降息，刺激经济增长。", "新能源技术的创新。")
    ]
}

questions = [
    ("利率上升，影响房地产市场。", "高利率对房地产有一定的冲击。"),
    ("油价大幅度下跌，能源公司面临挑战。", "未来智能城市的建设趋势越加明显。"),
    ("股票市场今日大涨，投资者乐观。", "持续上涨的市场让投资者感到满意。")
]

messages = [
    {"role": "system", "content": f"你帮我完成文本匹配，我给你2个句子，被[]包围，你判断它们是否匹配，回答是或不是，请参考如下示例："},
]

for key, values in examples_data.items():
    for value in values:
        messages.append({"role": "user", "content": f"第一句话是：{value[0]}，第二句话是：{value[1]}"})
        messages.append({"role": "assistant", "content": key})

for question in questions:

    msg = [{"role": "user", "content": f"根据上述参考列子，来判断以下两句是否相关，第一句话是：{question[0]}，第二句话是：{question[1]}"}]

    response = client.chat.completions.create(
        model=model,
        messages=messages + msg,
    )

    print(response.choices[0].message.content)

