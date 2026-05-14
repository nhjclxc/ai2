#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/26 17:55
# Module    : main.py
# explain   :
import os
from pathlib import Path

from dotenv import load_dotenv

from openai import OpenAI

load_dotenv(Path(__file__).parent.with_name(".env"))
qwen_api_key = os.getenv("QWEN_API_KEY")
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
model = "qwen-plus"
client = OpenAI(
    api_key=qwen_api_key,
    base_url=base_url
)

def test():
    with client.chat.completions.stream(
            model = model,
            messages=[
                {"role": "user", "content": "1+2+3+...+100=?"}
            ]
        ) as stream:
        for event in stream:
            chunk = getattr(event, "chunk", None)
            if not chunk or not hasattr(chunk, "choices"):
                continue
            delta = chunk.choices[0].delta
            if delta.content:
                print(delta.content, end="", flush=True)

# test()

# 金融文本分类数据，https://github.com/smoothnlp/FinancialDatasets

# 示例数据
examples_data = {
    '新闻报道': '今日，股市经历了一轮震荡，受到宏观经济数据和全球贸易紧张局势的影响。投资者密切关注美联储可能的政策调整，以适应市场的不确定性。',
    '财务报告': '本公司年度财务报告显示，去年公司实现了稳步增长的盈利，同时资产负债表呈现强劲的状况。经济环境的稳定和管理层的有效战略执行为公司的健康发展奠定了基础。',
    '公司公告': '本公司高兴地宣布成功完成最新一轮并购交易，收购了一家在人工智能领域领先的公司。这一战略举措将有助于扩大我们的业务领域，提高市场竞争力',
    '分析师报告': '最新的行业分析报告指出，科技公司的创新将成为未来增长的主要推动力。云计算、人工智能和数字化转型被认为是引领行业发展的关键因素，投资者应关注这些趋势'
}

# 提问数据
questions = [
    "今日，央行发布公告宣布降低利率，以刺激经济增长。这一降息举措将影响贷款利率，并在未来几个季度内对金融市场产生影响。",
    "ABC公司今日发布公告称，已成功完成对XYZ公司股权的收购交易。本次交易是ABC公司在扩大业务范围、加强市场竞争力方面的重要举措。据悉，此次收购将进一步巩固ABC公司在行业中的地位，并为未来业务发展提供更广阔的发展空间。详情请见公司官方网站公告栏",
    "公司资产负债表显示，公司偿债能力强劲，现金流充足，为未来投资和扩张提供了坚实的财务基础。",
    "最新的分析报告指出，可再生能源行业预计将在未来几年经历持续增长，投资者应该关注这一领域的投资机会",
    "小明喜欢小新哟",
    "美国记者晚宴发生枪击，特朗普被紧急撤离，嫌疑人已被捕"
]


messages = [
    {"role": "system", "content": "你是金融专家，将文本分类为['新闻报道', '财务报道', '公司公告', '分析师报告']，不清楚的分类为'不清楚类别' 下面有示例："},
]

# 将示例数据添加到message里面，类似聊天记录
for key, value in examples_data.items():
    # 构造llm与用户聊天的分类数据
    # value 是文本数据，对应的key就是llm给出的答案
    messages.append({"role": "user", "content": value})
    messages.append({"role": "assistant", "content": key})

# 调用llm来实现功能，便利每一个问题，让llm基于已有的聊天记录返回推理结果
for question in questions:

    response = client.chat.completions.create(
        model = model,
        # 将question拼接到message里面，注意不要改变messages，否则下一个遍历的messages就会污染了
        messages=messages + [{"role": "user", "content": f"按照示例，回答这段文本的分类类别：{question}"}]
    )
    print(f"question: {question}")
    print(f"answer :{response.choices[0].message.content}")
    print()