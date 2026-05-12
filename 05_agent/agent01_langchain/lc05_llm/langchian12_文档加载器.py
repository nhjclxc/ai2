#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/10 10:59
# Module    : langchian12_文档加载器.py
# explain   :

from langchain_community.document_loaders import CSVLoader, JSONLoader, PyPDFLoader, TextLoader


# langchain支持的所有文档加载器:https://docs.langchain.com/oss/python/integrations/document_loaders
# 下面只对以下三个常用的进行学习
# CSVLoader
# JSONLoader
# PyPDFLoader
# TestLoader
# 所有的文档加载器都要实现一个BaseLoader的接口
# 所有的文档加载器最终都是返回ClassDocument实例对象


# ===================================== CSVLoader =====================================

def test_csv_loader():

    loader = CSVLoader(
        file_path="./../data/advertising.csv",
        csv_args={
            "delimiter": ",", # 指定csv文件每一个列的分隔符
            "quotechar": '"',   # 使用""去包裹一个整体
            # 指定表头,那么旧不会使用csv文件里面的表头,而会使用这里指定的表头
            # "fieldnames": ["type_id","type_TV","type_Radio","type_Newspaper","type_Sales","type_location"],
        }
    )
    # load() 方法一次性加载全部数据
    data = loader.load()
    # print(data)
    print(len(data))
    data0 = data[0]
    print('data0.id ', data0.id)
    print(data0.type) # <class 'langchain_core.documents.base.Document'>
    print('data0.page_content ', data0.page_content, type(data0.page_content))
    print(data0.metadata)
    print(type(data0))
    data0_json = data0.to_json()
    print(data0_json, type(data0_json))
    print(data0_json.get('kwargs').get('page_content'))
    # print(data0.dict())
    # print(data0.json())

    print()

    # lazy_load()方法返回一个使用 yield 实现的迭代器, 因此要用for循环取遍历每一个数据

    # for itme in loader.lazy_load():
    #     print(itme)
    #     print()


    pass

# test_csv_loader()


# ===================================== JSONLoader =====================================
def test_json_loader():
    """
        使用lanchain里面的jsonloader必须额外安装一个包 " uv add jq ", JSONLoader底层依赖jq
    """

    json_loader = JSONLoader(
        file_path="./../data/json_loader.json",
        jq_schema=".", # 这个是jq语法表示抽取整个json文件的数据
        text_content=False, # 表示抽取的内容是不是字符串
        json_lines=False  # 表示这个文件是一个完整的json文件,而不是jsonL文件
    )

    data = json_loader.load()
    print(data)
    data0 = data[0]
    print(data0.page_content)
    print(data0.metadata)
    print(data0.type)
    print('data0.id ', data0.id)



    pass

# test_json_loader()

def test_json_loader2():
    """
        使用lanchain里面的jsonloader必须额外安装一个包 " uv add jq ", JSONLoader底层依赖jq
    """

    json_loader = JSONLoader(
        file_path="./../data/json_loader.json",
        jq_schema=".hobby", # 这个是jq语法表示抽取整个json文件的数据
        text_content=False, # 表示抽取的内容是不是字符串
        json_lines=False  # 表示这个文件是一个完整的json文件,而不是jsonL文件
    )

    data = json_loader.load()
    print(data)
    data0 = data[0]
    print(data0.page_content)
    print(data0.metadata)
    print(data0.type)
    print('data0.id ', data0.id)



    pass

# test_json_loader2()


def test_json_loader3():
    """
        使用lanchain里面的jsonloader必须额外安装一个包 " uv add jq ", JSONLoader底层依赖jq
    """

    json_loader = JSONLoader(
        file_path="./../data/json_loader_lines.jsonl",
        jq_schema=".", # 这个是jq语法表示抽取整个json文件的数据
        text_content=False, # 表示抽取的内容是不是字符串
        json_lines=True  # 表示这个文件是一个完整的json文件,而不是jsonL文件
    )

    data = json_loader.load()
    print(data)
    data0 = data[0]
    print(data0.page_content)
    print(data0.metadata)
    print(data0.type)
    print('data0.id ', data0.id)



    pass

# test_json_loader3()

def test_json_loader5():
    """
        使用lanchain里面的jsonloader必须额外安装一个包 " uv add jq ", JSONLoader底层依赖jq
    """

    json_loader = JSONLoader(
        file_path="./../data/json_loader_list.json",
        jq_schema=".[].name", # 这个是jq语法表示抽取整个json文件的数据
        text_content=False, # 表示抽取的内容是不是字符串
        json_lines=False  # 表示这个文件是一个完整的json文件,而不是jsonL文件
    )

    data = json_loader.load()
    print(data)
    data0 = data[0]
    print(data0.page_content)
    print(data0.metadata)
    print(data0.type)
    print('data0.id ', data0.id)



    pass

# test_json_loader5()

# ===================================== PyPDFLoader =====================================
def test_pdf_loader():
    """
        使用lanchain里面的 PyPDFLoader 必须额外安装一个包 " uv add pypdf ", PyPDFLoader 底层依赖 pypdf
    """

    # D:\code\py\ai2\05_agent\ai-agent road map.pdf
    # ./../../ai-agent road map.pdf

    loader = PyPDFLoader(
        file_path="./../../ai-agent road map.pdf",
        # mode: Literal["single", "page"] = "page",
    )
    print(loader)
    print(loader.source)
    data = loader.load()
    print(data)
    print(len(data))
    print(data[0])



    pass
# test_pdf_loader()


# TextLoader 和 文档加载器


def test_text_loader():

    loader = TextLoader(
        file_path="./../data/test_loader.txt",
        encoding="utf-8",
    )
    # TextLoader 返回的数据只有一个itme,即会全部返回所有txt文件的内容
    data = loader.load()
    print(data)
    print(len(data))
    data0 = data[0]
    print(data0.page_content)


    pass

# test_text_loader()


from langchain_text_splitters import RecursiveCharacterTextSplitter

def test_text_loader_split():
    # TextLoader 会一次性读取txt文档里面的所有内容
    # 如果文档太大则太占用内存,因此要使用文档分割器 RecursiveCharacterTextSplitter 对大文档进行分割

    loader = TextLoader(
        file_path="./../data/test_loader.txt",
        encoding="utf-8",
    )
    data = loader.load()

    # 创建文档分割器  递归字符文本分割器
    splitter = RecursiveCharacterTextSplitter(
        # 分割文档的字符
        separators=["\n\n", "\n", "。", "?", "？", "！", ".", "!", "?", " "],
        chunk_size=100, # 分割的最大字符数
        chunk_overlap=10, #分段之间允许重复的字符数
        length_function=len, # 统计字符个数的函数
    )

    # 将文档分割器应用于文档上
    split_data = splitter.split_documents(data)
    # type(split_data) -->>  list[Document]
    # data 被分割之后分割出来的 split_data 就是  list[Document],可以迭代遍历了
    # 即使用 splitter 将一个Doucument文档对象分割为多个Document文档对象
    print(split_data)
    print(len(split_data))
    print(split_data[0])
    print("="*50)
    print(split_data[1])




    pass

test_text_loader_split()


