#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/12 20:40
# Module    : file_history_store.py
# explain   :
import json
import os
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, messages_from_dict, message_to_dict

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
            json.dump(serialized, f, ensure_ascii=False, indent=4)

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)

if __name__ == "__main__":

    store = FileChatMessageHistory("data/history", "session001")



    pass