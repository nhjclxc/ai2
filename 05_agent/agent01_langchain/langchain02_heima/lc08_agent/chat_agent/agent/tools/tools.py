#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/17 15:41
# Module    : tools.py
# explain   :
import json
import os
import random
from datetime import datetime

from langchain_core.tools import tool

from langchain02_heima.lc08_agent.chat_agent.rag.rag_service import rag
from langchain02_heima.lc08_agent.chat_agent.utils.path_tool import get_abs_path


@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)

@tool(description="查询天气")
def get_weather(city: str) -> str:
    return f"城市{city}的天气为晴天，温度26摄氏度，空气湿度50%"

@tool(description="获取用户所在的城市")
def get_user_city() -> str:
    return random.choice(['厦门', '福州', '泉州'])

user_ids = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010]
# letters = "1234567890zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP"
# print("".join(random.choices(letters, k=5)))
@tool
def get_user_id() -> int:
    """
    获取当前用户ID
    """
    return random.choice(user_ids)

months = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06", "2025-07", "2025-08",
            "2025-09", "2025-10", "2025-11", "2025-12"]
@tool(description="获取当前月份")
def get_current_month() -> str:
    return random.choice(months)

@tool(description="从外部系统获取指定用户指定月份的数据")
def fetch_external_data(user_id: int, month: str) -> str:
    generate_external_data()

    try:
        return external_dict[user_id][month]
    except KeyError:
        print(f"找不到对应的对应用户{user_id},对应月份{month}的数据")
        return ""

external_dict = {}

def generate_external_data() -> dict:

    if len(external_dict) > 1:
        return external_dict

    external_path = get_abs_path("data/records.csv")

    if not os.path.exists(external_path):
        raise FileNotFoundError(f"外部数据文件{external_path} 不存在")

    with open(external_path, "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            data_arr = line.strip().split(",")
            #     "用户ID","特征","清洁效率","耗材","对比","时间"
            # external_dict[] = {}
            # external_dict[data_arr[0]] = {}

            user_id = int(data_arr[0].replace('"', ""))
            month = data_arr[5].replace('"', "")
            external_dict.setdefault(user_id, {})[month] = {
                    "特征": data_arr[1].replace('"', ""),
                    "清洁效率": data_arr[2].replace('"', ""),
                    "耗材": data_arr[3].replace('"', ""),
                    "对比": data_arr[4].replace('"', ""),
                }

    print('数据构造完毕！')

    return external_dict


@tool(description="检测是否切换提示词")
def fill_context_for_report() -> bool:
    return random.choice([True, False])

if __name__ == '__main__':
    # print(get_user_id.invoke({}))


    print(external_dict)
    generate_external_data()
    print(len(external_dict))
    print(external_dict)

    user_id_100202_data = fetch_external_data.invoke({"user_id": 1002, "month": "2025-02"})
    print('user_id_100202_data ', user_id_100202_data)