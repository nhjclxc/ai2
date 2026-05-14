#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/10 16:37
# Module    : langchian16_向量存储对象加入langchain调用链.py
# explain   :
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore

from langchain02_heima.lc00_core.model_helper import get_chat_openai, get_embedding_model

# 本文件基于langchian15_基于向量检索构建提示词.py，为的是 实现向量存储对象加入langchain调用链‘
# 即 RunnablePassthrough 的使用



chat_model = get_chat_openai(streaming=True)
embed_model = get_embedding_model()

message_prompt = ChatPromptTemplate.from_messages([
    # ('system', '以我提供的参考资料为主，简洁和专业的回答用户提出的问题，不要超出参考资料范围，参考资料：{context}'),
    ('system', '你是一个知识库问答助手。你必须严格依据“参考资料”回答问题。规则：1. 不允许使用参考资料以外的知识 2. 回答尽量简洁参考资料：{context}'),
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

# 要想将某个对象活方法加入langchian链，那么这个对象或方法必须实现Runnable接口，可是InMemoryVectorStore相关的类没有实现该接口
# 但是 InMemoryVectorStore 相关类实现了一个方法 as_retriever 可以返回一个 Runnable接口的子类实例对象
# 我们可以把这个子类实例对象加入langchain调用链，以达到将InMemoryVectorStore加入langchain调用链
# {'k': k} 会去搜索vector_store.similarity_search(input_text, 3)中的k: '3'
# retriever 的输入：用户的提问，输出：向量库中检索的资料
retriever = vector_store.as_retriever(search_kwargs={'k': 3})
# retriever 实现的功能类似 similarity_search

def print_prompt(x: PromptValue) -> PromptValue:
    print("="*50)
    print(f"用户提示词：{x.to_string()}")
    print("="*50)
    return x

def format_fun(docs: list[Document]) -> str:
    if not docs:
        return "无相关参考资料"

    strs = []
    for doc in docs:
        strs.append(doc.page_content)
    s = "[" + "。".join(strs) + "]"
    print("转化后的数据：", s)
    return s


# 首先使用dict作为一个链用来初始化数据
# RunnablePassthrough()在这里作为占位符
# retriever 这里返回的是 list[Document] 不能直接传递给 context ，因此后面需要在借一个转化数据的函数 format_fun
#       format_fun 函数的输入就是 retriever 的返回值即 list[Document]，输出就是 字典里面 context 要的类型即 str
# 第一个链模块提供一个整体的字典给后面第二个链模块message_prompt使用
# 注意：retriever 是整个chain的第一个组件
chain = (
    {"input": RunnablePassthrough(), "context": retriever | RunnableLambda(format_fun) }
    | message_prompt
    | RunnableLambda(print_prompt)
    | chat_model
    | StrOutputParser()
)

# 将 input_text 输入给 retriever 的同时内部还会将这份数据传递给 RunnablePassthrough() 占位符对应的 input
# 输入内容会在langchain内部分流一份数据给RunnablePassthrough占位符指定的key
resp = chain.stream(input_text)

for r in resp:
    print(r, end="", flush=True)


"""
res  [Document(id='id_6', metadata={}, page_content='减肥就是要少吃多练'), Document(id='id_3', metadata={}, page_content='最近每天都在做有氧运动进行减脂'), Document(id='id_1', metadata={}, page_content='今天开始严格控制饮食减少碳水摄入')]
转化后的数据： [减肥就是要少吃多练。最近每天都在做有氧运动进行减脂。今天开始严格控制饮食减少碳水摄入]
==================================================
用户提示词：System: 你是一个知识库问答助手。你必须严格依据“参考资料”回答问题。规则：1. 不允许使用参考资料以外的知识 2. 回答尽量简洁参考资料：[减肥就是要少吃多练。最近每天都在做有氧运动进行减脂。今天开始严格控制饮食减少碳水摄入]
Human: 用户提问：怎么减肥？
==================================================
减肥就是要少吃多练。可以每天进行有氧运动减脂，并严格控制饮食、减少碳水摄入。
进程已结束，退出代码为 0


"""