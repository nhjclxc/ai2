#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/6 21:07
# Module    : langchian10_redis_memory历史消息.py
# explain   :
import json

from typing import Sequence

import tiktoken
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import RunnableWithMessageHistory, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import messages_from_dict, message_to_dict, BaseMessage, HumanMessage, AIMessage

from sqlalchemy import Column, Integer, String, JSON, select, delete, DateTime

from langchain02_heima.lc00_core.model_helper import get_chat_openai
from langchain02_heima.lc05_llm.mysqldb.db_mysql_sync import Base, get_session_local, get_session
from langchain02_heima.lc05_llm.mysqldb.db_redis_sync import RedisClient


def print_prompt(x: PromptValue):
    print("="*20, " 打印当前提示词 ", "="*20)
    print(x.to_string())
    return x


# =================================== 1、实现 MySQLChatMessageHistory 相关功能 ===================================

# 在mysql数据库中一条消息存储一条记录，即一条 AiMessage存储一条，一条HumanMessage存储一条

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(32), nullable=False)
    message = Column(JSON, nullable=False)
    message_time = Column(DateTime, nullable=False)


class MySQLChatMessageHistory(BaseChatMessageHistory):
    """ 类比 FileChatMessageHistory 实现 MySQLChatMessageHistory 类 """

    def __init__(self, session_id: str, max_token: int = 200):
        self.session_id = session_id
        self.max_token = max_token
        self.encoding = tiktoken.encoding_for_model("gpt-4o")


    @property
    def messages(self) -> list[BaseMessage]:
        """ 获取数据库中当前 session_id 所对应的所有聊天数据 """

        try:
            with get_session(get_session_local()) as session:  # AsyncSession
                result = session.execute(
                    select(ChatHistory).where(ChatHistory.session_id == self.session_id).order_by(ChatHistory.id)
                )
                # {"type": "human", "data": {"content": "\u5c0f\u660e\u603b\u6709\u591a\u5c11\u53ea\u5ba0\u7269\uff1f", "additional_kwargs": {}, "response_metadata": {}, "type": "human", "name": null, "id": null}}
                chatHistorys: Sequence[ChatHistory] = result.scalars().all()
                messages_data = []
                for chatHistory in chatHistorys:
                    messages_data.append(chatHistory.message)
                return messages_from_dict(messages_data)
        except Exception as e:
            print(e)
            return []

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """ 将最新的消息加入到数据库中 """

        with get_session(get_session_local()) as session:  # Session

            # human, ai
            insert_messages = [ChatHistory(session_id=self.session_id, message=message_to_dict(message)) for message in messages]
            session.add_all(insert_messages)
            # session.commit()
            print(f"add_messages create ChatHistory result len {len(insert_messages)}")

    def add_messages2(self, messages: Sequence[BaseMessage]) -> None:
        """ 将最新的消息加入到数据库中, 并且限制数据库中该会话的token数量 """

        # 先获取 历史数据(逆序), 将当前传入的消息messages与历史消息一个一个计算token,
        # 当超出最大token时就丢弃后面所有的聊天记录,只保留最大token以内的聊天数据

        db_messages = self.messages

        with get_session(get_session_local()) as session:  # Session
            # 1 清空数据库中所有数据
            session.execute(delete(ChatHistory).where(ChatHistory.session_id == self.session_id))

            # 2 构造数据
            db_messages.extend(messages)

            # 3 计算 token
            insert_messages = []
            current_token = 0
            for db_msg in db_messages:
                encode_toekn = len(self.encoding.encode(db_msg.content))
                if current_token + encode_toekn > self.max_token:
                    break
                current_token += encode_toekn
                insert_messages.insert(0, db_msg)

            session.add_all(insert_messages)
            print(f"add_messages create ChatHistory result len {len(insert_messages)}")

    def add_messages3(self, messages: Sequence[BaseMessage]) -> None:

        db_messages = list(self.messages)

        # 1️⃣ 追加新消息
        db_messages.extend(messages)

        # 2️⃣ 从新到旧
        db_messages = list(reversed(db_messages))

        build_messages = []
        build_redis_messages = []
        current_mysql_token = 0
        current_redis_token = 0
        build_mysql_flag = False
        build_redis_flag = False

        # 3️⃣ token裁剪
        for msg in db_messages:

            token = len(self.encoding.encode(msg.content))

            if current_redis_token + token < self.max_token:
                current_redis_token += token
                build_redis_messages.append(msg)
            else:
                build_redis_flag = True

            if current_mysql_token + token < self.max_token:
                current_mysql_token += token
                build_messages.append(msg)
            else:
                build_mysql_flag = True

            if build_mysql_flag and build_redis_flag:
                break

        # 4️⃣ 恢复时间顺序
        build_messages.reverse()

        # 存数据库的同时存redis,以保持热数据

        # 5️⃣ 构造插入数据库的数据格式
        insert_messages = [ChatHistory(session_id=self.session_id, message=message_to_dict(m)) for m in build_messages]

        with get_session(get_session_local()) as session:
            # 先清空后新增所有
            session.execute( delete(ChatHistory).where(ChatHistory.session_id == self.session_id))
            session.add_all(insert_messages)
            print(f"add_messages create ChatHistory result len {len(insert_messages)}")

    def clear(self) -> None:
        """ 清空当前 session_id 所对应的所有聊天数据 """

        with get_session(get_session_local()) as session:  # Session
            session.execute(delete(ChatHistory).where(ChatHistory.session_id == self.session_id))

def test_mysqlChatMessageHistory():
    """ 测试 MySQLChatMessageHistory 的相关功能 """
    # 初始化数据库
    # init_db()

    mysqlChatMessageHistory = MySQLChatMessageHistory("session001")

    # 获取消息总数
    messages = mysqlChatMessageHistory.messages
    print(len(messages))
    if len(messages) > 0:
        print(messages[0])
        print(messages[0].content)

    # '{"data": {"id": null, "name": null, "type": "human", "content": "你是什么模型？", "additional_kwargs": {}, "response_metadata": {}}, "type": "human"}'
    # '{"data": {"id": null, "name": null, "type": "ai", "content": "我是基于 OpenAI GPT-5.5 的 ChatGPT。", "tool_calls": [], "usage_metadata": null, "additional_kwargs": {}, "response_metadata": {}, "invalid_tool_calls": []}, "type": "ai"}'
    mgs1 = HumanMessage("你是什么模型？")
    mgs2 = AIMessage("我是基于 OpenAI GPT-5.5 的 ChatGPT。")

    mysqlChatMessageHistory.add_messages([mgs1, mgs2])
    print(len(mysqlChatMessageHistory.messages))

    # 清空表结构
    # mysqlChatMessageHistory.clear()
    print(len(mysqlChatMessageHistory.messages))


# =================================== 2、实现 llm 的 chat 聊天 相关功能 ===================================

def mysql_chat_history():

    # 获取聊天模型
    chat = get_chat_openai(streaming=True)

    # 构造消息模板
    chat_prompt_template = ChatPromptTemplate.from_messages([
        ('human', "你是一个聊天小助手，根据human与ai的聊天记录，实现相关功能。注意：只要简单回答不要有过多的废话"),
        MessagesPlaceholder(variable_name="chat_historys"),
        ('human', "用户消息：{input}")
    ])

    # 构造一个基础的聊天链
    base_chain = (
        chat_prompt_template
        | RunnableLambda(print_prompt)
        | chat
        | StrOutputParser()
    )

    # 创建消息记忆功能
    chat_history_store: dict[str, MySQLChatMessageHistory] = {}
    def get_history(session_id: str) -> MySQLChatMessageHistory:
        if session_id not in chat_history_store:
            chat_history_store[session_id] = MySQLChatMessageHistory(session_id)
        return chat_history_store[session_id]

    # 将基础聊天链chain 与 消息记忆功能 绑定
    chat_history_chain = RunnableWithMessageHistory(
        runnable=base_chain,
        get_session_history=get_history,
        input_messages_key="input",
        history_messages_key="chat_historys",
    )

    # 配置当前的会话信息
    session_config = {"configurable": {"session_id": "session001"}}

    # 聊天
    human_inputs = ["超超有5本地理书", "润润有6本英语数", "润润又买了2本数学书", "总共有几个人?有几本书?每个人分别有基本书?"]
    # buffer = StringIO()
    for i, input in enumerate(human_inputs):
        resp = chat_history_chain.stream(input={"input": input}, config=session_config)
        if i == len(human_inputs) - 1:
            for chunk in resp:
                print(chunk, end="", flush=True)
                # 写入buffer
                # buffer.write(chunk)
        # print(f"最终ai回答: {buffer.getvalue()}")
        print()

    pass


def test_tokenizer():

    encoding = tiktoken.encoding_for_model("gpt-4o")

    text = "hello world 你好啊"
    text = '{"data": {"id": null, "name": null, "type": "human", "content": "你是什么模型？", "additional_kwargs": {}, "response_metadata": {}}, "type": "human"}'

    tokens = encoding.encode(text)

    # print(tokens)
    print(len(tokens))
    pass


def gen_redis_key(session_id: str) -> str:
    return f"chat:history:{session_id}"

def test_redis():
    session_id = "session001"
    redis_client = RedisClient()
    # msg0 = SystemMessage("你是一个聊天小助手")
    # mgs1 = HumanMessage("你是什么模型？")
    # mgs2 = AIMessage("我是基于 OpenAI GPT-5.5 的 ChatGPT。")
    # mgs3 = HumanMessage("你最拿手的活是什么？简单一句话回答")
    # mgs4 = AIMessage("我最拿手的是把复杂技术问题快速定位清楚，并直接给出能落地的解决方案。")
    # messages = [msg0, mgs1, mgs2, mgs3, mgs4]
    # for msg in messages:
    #     msg_json_str = json.dumps(message_to_dict(msg), encoding="utf-8", ensure_ascii=False)
    #     print(msg_json_str)
    #     redis_client.lpush(gen_redis_key(session_id), msg_json_str)

    print("redis存储数据: ")
    all_msgs = redis_client.lrange(gen_redis_key(session_id))
    all_msgs_dict = []
    for msg in all_msgs:
        all_msgs_dict.append(json.loads(msg))

    all_messages = messages_from_dict(all_msgs_dict)
    print(all_messages, type(all_messages), type(all_messages[0]) if len(all_messages) > 0 else None)


    pass
if __name__ == "__main__":
    test_mysqlChatMessageHistory()

    # mysql_chat_history()

    # test_tokenizer()

    pass