"""
基于Streamlit完成WEB网页上传服务

pip install streamlit

Streamlit：当WEB页面元素发生变化，则代码重新执行一遍

启动 streamlit 网页程序：
(agent01_langchain) D:\code\py\ai2\05_agent\agent01_langchain\lc06_rag>uv run streamlit run app_file_uploader.py
2026-05-10 21:13:30.734 Uvicorn server started on 0.0.0.0:8501

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.4:8501

"""
import time

import streamlit as st

import sys
print(sys.executable)

import os
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.append(BASE_DIR)

from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")

# 定义file_uploader上传组件
uploader_file = st.file_uploader(
    "请上传TXT文件",
    type=['txt'],
    accept_multiple_files=False,    # False表示仅接受一个文件的上传
)


# streamlit 当外部元素的变化，整个脚本都会重新执行一遍
# 因此要使用一个session_state来存储已经创建的对象

# session_state就是一个字典
if "service" not in st.session_state:
    # 将知识库对应加入到 st 服务里面
    st.session_state["service"] = KnowledgeBaseService()


if uploader_file is not None:
    # 提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024    # KB

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

    # get_value -> bytes -> decode('utf-8')
    text = uploader_file.getvalue().decode("utf-8")

    with st.spinner("载入知识库中。。。"):       # 在spinner内的代码执行过程中，会有一个转圈动画
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)
