#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/10 15:23
# Module    : langchian13_vector向量存储.py
# explain   :
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

from langchain02_heima.lc00_core.model_helper import get_embedding_model


# 存储向量 add_document
# 检索向量 similarity_search
# 删除向量 delete


def test_vector_memory_store1():
    # 内存向量数据库

    # 获取一个嵌入模型
    embedding_model = get_embedding_model()

    # 创建向量存储模型，将嵌入模型与向量存储模型板绑定
    vector_store = InMemoryVectorStore(embedding=embedding_model)

    # 准备要存入向量模型的数据

    # 和 "love" 相关的英文单词

    love_document_list = [
        Document(page_content="love"),  # 爱
        Document(page_content="affection"),  # 喜爱；感情
        Document(page_content="passion"),  # 热情；激情
        Document(page_content="romance"),  # 浪漫；爱情
        Document(page_content="adoration"),  # 崇拜；爱慕
        Document(page_content="fondness"),  # 喜欢；偏爱
        Document(page_content="devotion"),  # 奉献；挚爱
        Document(page_content="care"),  # 关心；照顾
        Document(page_content="kindness"),  # 善良；体贴
        Document(page_content="attachment"),  # 依恋；依附
        Document(page_content="intimacy"),  # 亲密；亲近
        Document(page_content="desire"),  # 渴望；欲望
        Document(page_content="crush"),  # 暗恋
        Document(page_content="beloved"),  # 心爱的人
        Document(page_content="cherish"),  # 珍惜；珍爱
    ]
    love_document_id_list = [f"id_{i+1}" for i in range(len(love_document_list))]

    love_cn_list = [
        "喜欢", "热爱", "关心", "珍惜", "陪伴", "守护", "思念", "温柔", "亲情", "友情", "爱情", "依恋", "牵挂",  "包容", "付出",
    ]
    love_cn_id_list = [f"id_cn_{i+1}" for i in range(len(love_cn_list))]

    # 将数据存入向量存储，存入数据的时候要文本和对应的id要一对一对的存入
    # add_documents 加入的数据必须是document对象
    res = vector_store.add_documents(documents=love_document_list, ids=love_document_id_list)
    print('res ', res)  # 返回存入的对应id
    # add
    res_cn = vector_store.add_texts(texts=love_cn_list, ids=love_cn_id_list)
    print('res_cn ', res_cn)  # 返回存入的对应id

    # 搜索文档, 第一个是指要查询的文本，第二个参数是相似度的top-k
    search_res = vector_store.similarity_search("like", 3)
    print('search_res ', search_res)

    # 删除对应文档
    delete_ids=[]
    if len(search_res) > 0:
        for sres in search_res:
            delete_ids.append(sres.id)
    print('delete_ids ', delete_ids)
    vector_store.delete(ids=delete_ids)
    # 再次搜索判断文档是否删除成功
    search_res = vector_store.similarity_search("like", 3)
    print('search_res 2 ', search_res)



    pass

# test_vector_memory_store1()



def test_vector_chroma_store1():
    # 文件向量数据库
    # uv add langchain_chroma chromadb
    from langchain_chroma import Chroma

    embedding_model = get_embedding_model()
    # 创建向量存储模型，将嵌入模型与向量存储模型板绑定
    file_vector_store = Chroma(
        collection_name="chroma_store", # 当前向量存储器的名字，类似于表名
        embedding_function=embedding_model, # 嵌入模型
        persist_directory=".\\..\\data\\output\\chroma_store"
    )
    vector_store  = file_vector_store

    # 准备要存入向量模型的数据

    # 和 "love" 相关的英文单词

    love_document_list = [
        Document(page_content="love"),  # 爱
        Document(page_content="affection"),  # 喜爱；感情
        Document(page_content="passion"),  # 热情；激情
        Document(page_content="romance"),  # 浪漫；爱情
        Document(page_content="adoration"),  # 崇拜；爱慕
        Document(page_content="fondness"),  # 喜欢；偏爱
        Document(page_content="devotion"),  # 奉献；挚爱
        Document(page_content="care"),  # 关心；照顾
        Document(page_content="kindness"),  # 善良；体贴
        Document(page_content="attachment"),  # 依恋；依附
        Document(page_content="intimacy"),  # 亲密；亲近
        Document(page_content="desire"),  # 渴望；欲望
        Document(page_content="crush"),  # 暗恋
        Document(page_content="beloved"),  # 心爱的人
        Document(page_content="cherish"),  # 珍惜；珍爱
    ]
    love_document_id_list = [f"id_{i+1}" for i in range(len(love_document_list))]

    love_cn_list = [
        "喜欢", "热爱", "关心", "珍惜", "陪伴", "守护", "思念", "温柔", "亲情", "友情", "爱情", "依恋", "牵挂",  "包容", "付出",
    ]
    love_cn_id_list = [f"id_cn_{i+1}" for i in range(len(love_cn_list))]

    # 将数据存入向量存储，存入数据的时候要文本和对应的id要一对一对的存入
    # add_documents 加入的数据必须是document对象
    res = vector_store.add_documents(documents=love_document_list, ids=love_document_id_list)
    print('res ', res)  # 返回存入的对应id
    # add
    res_cn = vector_store.add_texts(texts=love_cn_list, ids=love_cn_id_list)
    print('res_cn ', res_cn)  # 返回存入的对应id

    # 搜索文档, 第一个是指要查询的文本，第二个参数是相似度的top-k
    search_res = vector_store.similarity_search("like", 3)
    print('search_res ', search_res)

    # 删除对应文档
    delete_ids=[]
    if len(search_res) > 0:
        for sres in search_res:
            delete_ids.append(sres.id)
    print('delete_ids ', delete_ids)
    vector_store.delete(ids=delete_ids)
    # 再次搜索判断文档是否删除成功
    search_res = vector_store.similarity_search("like", 3)
    print('search_res 2 ', search_res)

    pass


test_vector_chroma_store1()



