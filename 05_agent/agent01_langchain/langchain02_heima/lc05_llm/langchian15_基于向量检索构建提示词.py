#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/10 16:37
# Module    : langchian15_基于向量检索构建提示词.py
# explain   :
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.vectorstores import InMemoryVectorStore

from langchain02_heima.lc00_core.model_helper import get_chat_openai, get_embedding_model

chat_model = get_chat_openai(streaming=True)
embed_model = get_embedding_model()

message_prompt = ChatPromptTemplate.from_messages([
    # ('system', '以我提供的参考资料为主，简洁和专业的回答用户提出的问题，不要超出参考资料范围，参考资料：{content}'),
    ('system', '你是一个知识库问答助手。你必须严格依据“参考资料”回答问题。规则：1. 不允许使用参考资料以外的知识 2. 回答尽量简洁参考资料：{content}'),
    ('human', '用户提问：{input}')
])

vector_store = InMemoryVectorStore(embed_model)
# 添加文本
texts = [
    # 与减肥有关
    "今天开始严格控制饮食减少碳水摄入",
    "晚上坚持慢跑五公里帮助燃烧脂肪",
    "最近每天都在做有氧运动进行减脂",
    "少吃高热量食物多吃蔬菜和蛋白质",
    "健身房训练计划已经坚持了一周时间",
    "减肥就是要少吃多练",
    "在减脂期间吃东西很重要,清淡少油控制卡路里摄入并运动起来",
    "跑步是很好的运动哦",

    # 与减肥无关
    "昨晚和朋友一起去看了一场电影放松",
    "新买的电脑性能很好运行速度非常快",
    "今天外面下着大雨天气变得很凉爽",
    "准备周末去周边城市旅游放松一下",
    "最近工作任务比较多每天都很忙碌",
]
vector_store.add_texts(texts=texts, ids=[f"id_{i+1}" for i in range(len(texts))])

input_text = "怎么减肥？"

# 检索向量库，把知识库里面高度相关的数据拿出来使用
res = vector_store.similarity_search(input_text, 3)
print('res ', res)

# 把document文档转化为字符串，放入prompt提示词content里面
contents = [r.page_content for r in res]
content_str = "[" + '。\n'.join(contents) + "]"
print('content_str ', content_str)

def print_prompt(x: PromptValue) -> PromptValue:
    print("="*50)
    print(f"用户提示词：{x.to_string()}")
    print("="*50)
    return x

chain = (
    message_prompt
    | RunnableLambda(print_prompt)
    | chat_model
    | StrOutputParser()
)

resp = chain.stream(input={
    "content": content_str,
    "input": input_text
})

for r in resp:
    print(r, end="", flush=True)


