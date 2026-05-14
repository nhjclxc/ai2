#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/11 22:04
# Module    : rag.py
# explain   :
from typing import Any

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

from langchain02_heima.lc06_rag import config_data
from langchain02_heima.lc06_rag.knowledge_base import KnowledgeBaseService
from langchain02_heima.lc06_rag.file_history_store import FileChatMessageHistory

def print_prompt(x):
    print("=" * 50)
    print("提示词：", x.to_string())
    print("=" * 50)
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

class RagService:
    def __init__(self):

        self.vector_store = KnowledgeBaseService()

        from langchain_core.prompts import MessagesPlaceholder
        self.prompt_template = ChatPromptTemplate.from_messages([
            ('system', '以我提供的已知参考资料为主，简洁和专业的回答用户提问的问题，参考资料：{context}.'),
            MessagesPlaceholder(variable_name="chat_historys"),
            ('human', '请回答用户提问：{input}')
        ])

        self.chat_model = config_data.chat_model

        self.__chain = None

        # 本地文件聊天历史记录
        self.history_store_dict: dict[str, FileChatMessageHistory] = {}


    def get_chain(self):
        if self.__chain is None:
            self.__chain = self.__gen_chain()
        return self.__chain

    def __gen_chain(self):
        """
            构造大模型调用链
        """
        retriever = self.vector_store.get_retriever()

        def fromat_retriever_input(x: dict[str, str]) -> str:
            # x --->>> {'input': '我的体重是180斤，身高是178cm，请给我对应的尺码推荐', 'chat_historys': []}
            # 由上输出可知，当加入历史消息RunnableWithMessageHistory后，输入到 retriever 的数据变为了dict，
            # 但是 retriever 只需要 x 字典里面的input数据。因此，我们只需要对x进行转化一下，把 x['input'] 送到 retriever 里面即可
            # print('tmp .... ', x)
            return x.get('input')

        def tmp(x: dict[str, Any]) -> dict[str, str]:
            # x --- >>> .... {'input': {'input': '我的体重是180斤，身高是178cm，请给我对应的尺码推荐', 'chat_historys': []}, 'context': '[身高：170-178cm， 体重：130-150斤，建议尺码XL。\n身高：175-182cm， 体重：145-165斤，建议尺码2XL。。身高：175-182cm， 体重：145-165斤，建议尺码2XL。\n身高：178-185cm， 体重：160-180斤，建议尺码3XL。。身高：178-185cm， 体重：160-180斤，建议尺码3XL。\n身高：180-190cm， 体重：180-210斤，建议尺码4XL。\n身高：190cm+，体重：210斤+，建议尺码5XL。]'}
            # 根据以上输出可知，我们 prompt_template 要的 chat_historys 数据 在 x['input']['input'] 里面，
            # 因此只需要把这个数据解析出来，构造一个包含 'chat_historys', 'context', 'input' 三个key的新字典即可
            new_dict = {}
            new_dict['context'] = x['context']
            new_dict['input'] = x['input']
            new_dict['chat_historys'] = x.get('input').get('chat_historys')
            print('x .... ', x)
            print('new_dict .... ', new_dict)
            return new_dict

        chain = (
            {
                "input": RunnablePassthrough(),
                #  message: input.texts should be array
                # self.vectorstore.similarity_search(query, **kwargs_)
                "context": RunnableLambda(fromat_retriever_input) | retriever | RunnableLambda(format_fun)
            }
            # KeyError: "Input to ChatPromptTemplate is missing variables {'chat_historys'}.  Expected: ['chat_historys', 'context', 'input'] Received: ['input', 'context']\nNote: if you intended {chat_historys} to be part of the string and not a variable, please escape it with double curly braces like: '{{chat_historys}}'.\nFor troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/INVALID_PROMPT_INPUT "
            # 意思是需要三个参数，'chat_historys', 'context', 'input'，但是只接收到两个参数 'input', 'context'，
            # 也就是说，还有一个参数 'chat_historys' 丢失掉了
            # 因此需要继续对输入数据进行转化
            | RunnableLambda(tmp)
            | self.prompt_template
            | RunnableLambda(print_prompt)
            | self.chat_model
            | StrOutputParser()
        )
        # return chain

        def get_history(session_id) -> FileChatMessageHistory:
            if session_id not in self.history_store_dict:
                self.history_store_dict[session_id] = FileChatMessageHistory("./data/history", "session001")
            return self.history_store_dict[session_id]

        history_chain = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=get_history,
            input_messages_key="input",
            history_messages_key="chat_historys",
        )

        return history_chain


if __name__ == "__main__":

    service = RagService()
    # resp = service.get_chain().stream("我的体重是180斤，身高是178cm，请给我对应的尺码推荐")  # 身高 ≤ 185 cm → 推荐 **3XL**
    # # resp = service.get_chain().stream("我的体重是180斤，身高是189cm，请给我对应的尺码推荐")  # 身高 > 185 cm → 推荐 **4XL**
    # for res in resp:
    #     # print(res.content, end="", flush=True)
    #     print(res, end="", flush=True)

    session_config = {"configurable": {"session_id": "session001"}}
    resp = service.get_chain().stream(
        input={"input": "我的体重是120斤，身高是169cm，请给我对应的尺码推荐"},
        config=session_config
    )
    for res in resp:
        print(res, end="", flush=True)


"""

rag：
    离线：给模型提供未来的知识文档，私有文档，规避模型幻觉
    在线：将用户提出的问题先经过rag进行私有知识库进行检索，获取私有的内部参考资料，同步组装新的提示词询问大模型获取结果
            用户的提问会被转化为向量，会去向量库中匹配最相近的内容，将匹配到的最相近的内容和在向量库中得到的数据同步发给llm以得到想要的结果

"""