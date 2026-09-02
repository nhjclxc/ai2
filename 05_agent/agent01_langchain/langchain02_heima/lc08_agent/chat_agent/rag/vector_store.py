#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/16 21:47
# Module    : vector_store.py
# explain   :

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain02_heima.lc08_agent.chat_agent.model.factory import embed_model
from langchain02_heima.lc08_agent.chat_agent.utils.file_handler import read_file, get_text_md5, save_file, pdf_loader, \
    list_dir_with_allowed_types, txt_loader
from langchain02_heima.lc08_agent.chat_agent.utils.path_tool import get_abs_path


class VectorStoreService:

    def __init__(self):

        self.vector_store = Chroma(
            collection_name="vector_store",
            embedding_function=embed_model,
            persist_directory=get_abs_path("output"),
        )

        self.spliter = RecursiveCharacterTextSplitter(
            separators=[" ", "\n", "\t", "\t", "\t", "\t", "\t", "\t", "\t"],
            chunk_size=200,
            chunk_overlap=20,
            length_function=len,
        )

        self.md5_file_path = "data/md5.txt"


    def load_text(self, text_data: str):

        from datetime import datetime
        t1 = datetime.now()
        # 读取目前所有已经保存的数据
        md5_text = read_file(self.md5_file_path)
        md5_datas = md5_text.splitlines()
        t2 = datetime.now()

        split_data = self.spliter.split_text(text_data)
        t3 = datetime.now()

        save_md5s: list[str] = []
        save_docs: list[str] = []

        for data in split_data:
            data_md5 = get_text_md5(data)
            if data_md5 in md5_datas or data_md5 in save_md5s:
                continue
            save_md5s.append(data_md5)
            save_docs.append(data)

        if len(save_docs) == 0:
            return 0

        t4 = datetime.now()

        if len(save_md5s) > 1:
            save_md5s_data = "\n".join(save_md5s) +"\n"
        else:
            save_md5s_data = save_md5s[0] + "\n"
        save_file(self.md5_file_path, save_md5s_data)
        t5 = datetime.now()

        print('t5 - t4', t5 - t4)
        print('t4 - t3', t4 - t3)
        print('t3 - t2', t3 - t2)
        print('t2 - t1', t2 - t1)
        self.vector_store.add_texts(save_docs)
        t6 = datetime.now()
        print('t6 - t5', t6 - t5)
        print('t6 - t1', t6 - t1)

        return len(save_docs)

    def load_document(self, docs: list[Document]):

        from datetime import datetime
        t1 = datetime.now()
        # 读取目前所有已经保存的数据
        md5_text = read_file(self.md5_file_path)
        md5_datas = md5_text.splitlines()

        split_docs = self.spliter.split_documents(docs)

        save_md5s: list[str] = []
        save_docs: list[str] = []

        for data in split_docs:
            data_md5 = get_text_md5(data.page_content)
            if data_md5 in md5_datas or data_md5 in save_md5s:
                continue
            save_md5s.append(data_md5)
            save_docs.append(data.page_content)

        if len(save_md5s) == 0:
            return 0

        if len(save_md5s) > 1:
            save_md5s_data = "\n".join(save_md5s) +"\n"
        else:
            save_md5s_data = save_md5s[0] + "\n"
        save_file(self.md5_file_path, save_md5s_data)
        t5 = datetime.now()

        self.vector_store.add_texts(save_docs)
        t6 = datetime.now()
        print('t6 - t5', t6 - t5)
        print('t6 - t1', t6 - t1)

        return len(save_docs)

    def get_retriever(self, k: int = 3):
        return self.vector_store.as_retriever(search_kwargs={'k': k})



if __name__ == '__main__':

    data = read_file("data/故障排除.txt")

    vector_store = VectorStoreService()
    # save_len = vector_store.load_text(data)
    # print('save_len = ', save_len)

    for path in list_dir_with_allowed_types("data", ["txt"]):
        save_len2 = vector_store.load_document(txt_loader(path))
        print('save_len2 = ', save_len2)
