#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/29 20:32
# Module    : langchain05_嵌入模型.py
# explain   :


import os
from pathlib import Path
from dotenv import load_dotenv

from langchain02_heima.lc00_core.cosine_similarity import get_cos

load_dotenv(Path(__file__).parent.with_name(".env"))
openai_api_key = os.getenv("OPENAI_API_KEY")
qwen_api_key = os.getenv("QWEN_API_KEY")
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
model_chat = "qwen-plus"

os.environ["HTTPS_PROXY"] = "http://127.0.0.1:10808"  # 如果需要

# from langchain_openai import OpenAIEmbeddings
# embeddings = OpenAIEmbeddings(
#     model=model,
#     openai_api_key = qwen_api_key,
#     openai_api_base = base_url
# )

from langchain_community.embeddings import DashScopeEmbeddings

model_embed = "text-embedding-v3"
embeddings = DashScopeEmbeddings(
    model=model_embed,
    dashscope_api_key=qwen_api_key
)

xihuan_embed = embeddings.embed_query('喜欢')
print(len(xihuan_embed), xihuan_embed)

# strs = ["喜欢", "爱", "想", "love", "miss"]
strs = [
    "我喜欢你",
    "我爱你",
    "我想你",
    "I love you",
    "I miss you"
]
strs_embeds = embeddings.embed_documents(strs)
print(len(strs_embeds))
for i, val in enumerate(strs_embeds):
    for i2, val2 in enumerate(strs_embeds):
        print(f"{strs[i]}, {strs[i2]} --->>> {get_cos(val, val2)}")
    print("="*60)




