#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/6 21:07
# Module    : langchian09_memory历史消息.py
# explain   :
from typing import Sequence

from langchain_classic.chains.summarize.map_reduce_prompt import prompt_template
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import RunnableWithMessageHistory, RunnableLambda
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

from lc00_core.model_helper import get_chat_openai

def print_prompt(x: PromptValue):
    print("="*20, " 打印当前提示词 ", "="*20)
    print(x.to_string())
    return x


# 临时记忆 RunnableWithMessageHistory 和 InMemoryChatMessageHistory 配合使用

def in_memory01():

    chat = get_chat_openai(streaming=True)

    # prompt_template = PromptTemplate.from_template("根据用户的历史消息 {chat_historys}，用户当前输入 {input}，请给出回应。")
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "你是一个聊天助手，回答问题时，不要有过多的废话回答"),
        MessagesPlaceholder(variable_name="chat_historys"),
        ("human", "用户输入：{input}")
    ])
    # 构造一个基础的聊天chain链
    base_chain = (
        prompt_template
        | RunnableLambda(print_prompt)
        | chat
        | StrOutputParser()
    )

    # 创建一个字典用于存放用户的会话对象
    # 注意：chat_history_store就是存储用户历史小时的对象，这个对象是在内存中的，即未落盘，是临时的
    chat_history_store: dict[str, InMemoryChatMessageHistory] = {}
    # 定义一个函数用于给 内部创建用户会话对象
    def gen_history(session_id: str) -> InMemoryChatMessageHistory:
        """ 生成 session_id 对应的会话历史记录对象 """
        if session_id not in chat_history_store:
            # 没有当前 session_id 的历史消息对象则创建一个
            chat_history_store[session_id] = InMemoryChatMessageHistory()
        print(f"[DEBUG] 当前session: {session_id}, 历史条数: {len(chat_history_store[session_id].messages)}")
        return chat_history_store[session_id]

    # 将 基础聊天base_chain链 与 存储历史消息对象的方法绑定
    chat_history_chain = RunnableWithMessageHistory(
        runnable=base_chain,
        get_session_history=gen_history,
        input_messages_key="input",
        history_messages_key="chat_historys",
    )


    # 如果直接如下调用就会报错
    # print(chat_history_chain.invoke(input={"input": "小明有一只猫"}))
    # ValueError: Missing keys ['session_id'] in config['configurable'] Expected keys are ['session_id'].
    # When using via .invoke() or .stream(), pass in a config;
    # e.g., chain.invoke({'input': 'foo'}, {'configurable': {'session_id': '[your-value-here]'}})

    # 配置当前会话的 session_id  下面是一个固定的写法
    session_config = {"configurable": {"session_id": "session001"}}

    # 模拟聊天
    print(chat_history_chain.invoke(input={"input": "小明有一只猫"}, config=session_config))
    print(chat_history_chain.invoke(input={"input": "小明有两只狗"}, config=session_config))
    print(chat_history_chain.invoke(input={"input": "小红又给小明送了狗的两倍加1的鹦鹉？"}, config=session_config))
    print(chat_history_chain.invoke(input={"input": "小明总有多少只宠物？"}, config=session_config))

    pass

# in_memory01()


# 长期记忆

# 注意：FileChatMessageHistory 类的基础代码来自 langchain_core.runnables.history.py文件官方提供的示例代码

import json
import os
from langchain_core.messages import messages_from_dict, message_to_dict, BaseMessage


class FileChatMessageHistory(BaseChatMessageHistory):
    storage_path: str
    session_id: str
    file_path: str

    def __init__(self, storage_path: str, session_id: str):
        self.storage_path = storage_path
        self.session_id = session_id
        self.file_path = os.path.join(storage_path, session_id + ".json")
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    @property
    def messages(self) -> list[BaseMessage]:
        """ 获取持久化的消息，并且将获取到的消息转化为 list[BaseMessage] 类型 """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
            return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """  """
        # 这里的 list(self.messages) 实际就是  def messages(self) -> list[BaseMessage]:
        # 加了 @property 注解 那么这个方法可以被当作属性来使用
        # all_messages = list(self.messages) 表示拿到所有的历史消息
        all_messages = list(self.messages)  # Existing messages
        # 表示将当前消息加入已有的历史消息，构成当前最新的所有消息
        all_messages.extend(messages)  # Add new messages

        # 序列化
        serialized = [message_to_dict(message) for message in all_messages]
        # 写文件
        # 将当前所有的最新消息all_messages全量写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(serialized, f)

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)

def file_memory01():
    """ 实现文件持久化的聊天记忆功能 """

    chat = get_chat_openai(streaming=True)

    # prompt_template = PromptTemplate.from_template("根据用户的历史消息 {chat_historys}，用户当前输入 {input}，请给出回应。")
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "你是一个聊天助手，回答问题时，不要有过多的废话回答"),
        MessagesPlaceholder(variable_name="chat_historys"),
        ("human", "用户输入：{input}")
    ])
    # 构造一个基础的聊天chain链
    base_chain = (
        prompt_template
        | RunnableLambda(print_prompt)
        | chat
        | StrOutputParser()
    )

    file_path = ".\\..\\data\\output\\messages"

    # 创建一个字典用于存放用户的会话对象
    # 注意：chat_history_store就是存储用户历史小时的对象，这个对象是在内存中的，即未落盘，是临时的
    chat_history_store: dict[str, FileChatMessageHistory] = {}
    # 定义一个函数用于给 内部创建用户会话对象
    def gen_history(session_id: str) -> FileChatMessageHistory:
        """ 生成 session_id 对应的会话历史记录对象 """
        if session_id not in chat_history_store:
            # 没有当前 session_id 的历史消息对象则创建一个
            chat_history_store[session_id] = FileChatMessageHistory(file_path, session_id)
        print(f"[DEBUG] 当前session: {session_id}, 历史条数: {len(chat_history_store[session_id].messages)}")
        return chat_history_store[session_id]

    # 将 基础聊天base_chain链 与 存储历史消息对象的方法绑定
    chat_history_chain = RunnableWithMessageHistory(
        runnable=base_chain,
        get_session_history=gen_history,
        input_messages_key="input",
        history_messages_key="chat_historys",
    )

    # 配置当前会话的 session_id  下面是一个固定的写法
    session_config = {"configurable": {"session_id": "session001"}}

    # 模拟聊天
    print(chat_history_chain.invoke(input={"input": "小明有一只猫"}, config=session_config))
    print(chat_history_chain.invoke(input={"input": "小明有两只狗"}, config=session_config))
    print(chat_history_chain.invoke(input={"input": "小红又给小明送了狗的两倍加1的鹦鹉？"}, config=session_config))
    print(chat_history_chain.invoke(input={"input": "小明总有多少只宠物？"}, config=session_config))

    # 历史消息是在每次 invoke() 调用结束后自动落盘的
    # 即，每一次invoke结束后就会去调用FileChatMessageHistory的add_messages方法是是西安历史消息落盘
    """
    invoke()
      ↓
    读取历史（messages）
      ↓
    调用模型
      ↓
    add_messages() ← ⭐这里触发写文件
      ↓
    返回结果
    """
    pass

# file_memory01()


# 下面将类比 FileChatMessageHistory 实现 MySQLChatMessageHistory 类
class MySQLChatMessageHistory(BaseChatMessageHistory):

    def __init__(self, mysql_uri: str, session_id: str):
        self.mysql_uri = mysql_uri
        self.session_id = session_id

    @property
    def messages(self) -> list[BaseMessage]:
        pass


    def add_message(self, message: BaseMessage) -> None:
        pass

    def clear(self) -> None:
        pass

