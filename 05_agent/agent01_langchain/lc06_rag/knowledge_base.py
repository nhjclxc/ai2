#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/10 21:15
# Module    : knowledge_base.py
# explain   :

import hashlib
import os.path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config_data as config


def get_text_md5(text: str, encoding = "utf-8") -> str:
    """
        获取 对应字符串的 md5值，并且返回
    :param encoding: "utf-8"
    :param text: 待产生md5的字符串
    :return: 计算的md5值
    """
    md5_val = hashlib.md5(text.encode(encoding)).hexdigest()
    return md5_val

def check_md5(md5_val) -> bool:
    """
        判断传入的 md5_val 是否已经出现过
    :param md5_val: 待判断的 md5 值
    :return: 出现过返回True，没出现过返回False
    """
    if not os.path.exists(config.md5_file_path):
        # 创建该文件
        open(config.md5_file_path, "w", encoding="utf-8").close()
        return False

    with open(config.md5_file_path, "r", encoding="utf-8") as f:
        file_md5_val = f.read()
        file_md5s = file_md5_val.split("\n")
        for file_md5 in file_md5s:
            if file_md5 == md5_val:
                return True

    return False


def save_md5(md5_vals: str | list[str]):
    """
        将目标 md5_val 对应的数据保存
    :param md5_vals: 要保存的md5数据
    """
    if not md5_vals:
        return

    if isinstance(md5_vals, str):
        md5_vals = [md5_vals]

    lines = [
        md5.strip() + '\n'
        for md5 in md5_vals
        if md5.strip()
    ]

    with open(config.md5_file_path, 'a', encoding='utf-8') as f:
        f.writelines(lines)



class KnowledgeBaseService():
    """
        保存知识库数据
    """

    def __init__(self):

        os.makedirs(config.persist_directory, exist_ok=True)

        # 本地向量库
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=config.embed_model,
            persist_directory=config.persist_directory
        )

        # 文本分割器
        self.splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", "。", "?", "？", "！", ".", "!", "?", " "],
            chunk_size=100,         # 分割的最大字符数
            chunk_overlap=50,       #分段之间允许重复的字符数
            length_function=len,    # 统计字符个数的函数
        )


    def get_retriever(self, k = 3) -> VectorStoreRetriever:
        return self.vector_store.as_retriever(search_kwargs={'k': k})


    def upload_by_str(self, text, file_name) -> list[str]:
        # print('KnowledgeBaseService.upload_by_str.file_name ', file_name)
        # print('KnowledgeBaseService.upload_by_str.text ', text)

        # 手动构造 list[Document] 对象用于文本分割
        docs = [Document(page_content=text, file_name=file_name)]

        if len(text) > config.max_split_char_number:
            # 返回切割好的 list[Document]
            docs = self.splitter.split_documents(docs)
            # docs = self.splitter.split_text(text)
            print('docs ', len(docs))

        # 遍历每一个切割好的doc，计算对应的md5数据，判断是否已经存储过该数据
        save_docs: list[Document] = []
        save_md5s: list[str] = []
        for doc in docs:
            print('doc ', doc.page_content)
            md5_val = get_text_md5(doc.page_content)
            md5_flag = check_md5(md5_val)
            if md5_flag:
                print('重复数据跳保存 ', md5_val)
                continue

            # 上面是检测文件里面是否有出现过，下面是检测当前数组save_md5s是否有出现过
            if md5_val in save_md5s:
                print('重复数据跳保存 save_md5s ', md5_val)
                continue

            save_docs.append(doc)
            save_md5s.append(md5_val)

        if len(save_docs) == 0:
            return []

        res = self.vector_store.add_documents(save_docs)
        save_md5(save_md5s)
        return res



if __name__ == '__main__':
    kb_service = KnowledgeBaseService()

    # print("get_text_md5, ", kb_service.get_text_md5("hello world"))
    # print("get_text_md5, ", kb_service.get_text_md5("hello world"))
    # print("get_text_md5, ", kb_service.get_text_md5("hello world"))

    # kb_service.save_md5(kb_service.get_text_md5("hello"))
    # kb_service.save_md5(kb_service.get_text_md5("world"))
    # kb_service.save_md5(kb_service.get_text_md5("python"))
    # kb_service.save_md5(kb_service.get_text_md5("langchain"))
    # kb_service.save_md5(kb_service.get_text_md5("agent"))

    # checks = ['java', 'python', 'go']
    # for check_item in checks:
    #     md5_val = kb_service.get_text_md5(check_item)
    #     res = kb_service.check_md5(md5_val)
    #     print(f" check_md5('{check_item}') --->>> {res}, get_text_md5 = {md5_val}")

    # text = "身高：170-178cm\n体重：130-150斤\n建议尺码XL\n身高：175-178cm\n体重：135-150斤\n建议尺码XxL\n身高：170-188cm\n身高：170-188cm\n"
    # res = kb_service.upload_by_str(text, "a.txt")
    # print('res ', res)

    retriever = kb_service.get_retriever()
    resp = retriever.invoke("我的体重是180斤，请给我对应的尺码推荐")
    for res in resp:
        print(res.page_content)
        print()

    pass