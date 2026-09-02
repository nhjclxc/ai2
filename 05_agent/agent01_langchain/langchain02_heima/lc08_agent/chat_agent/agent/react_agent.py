#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/17 17:38
# Module    : react_agent.py
# explain   : 创建agent对象
from langchain.agents import create_agent

from langchain02_heima.lc08_agent.chat_agent.agent.tools.middleware import report_prompt_switch, log_before_model, \
    monitor_tool
from langchain02_heima.lc08_agent.chat_agent.agent.tools.tools import (rag_summarize, get_weather, get_user_city,
        get_user_id, get_current_month, fetch_external_data, fill_context_for_report)
from langchain02_heima.lc08_agent.chat_agent.model.factory import chat_model
from langchain02_heima.lc08_agent.chat_agent.utils.file_handler import prompt_main_prompt

tools = [rag_summarize, get_weather, get_user_city, get_user_id, get_current_month, fetch_external_data,
            fill_context_for_report]

middlewares = [monitor_tool, log_before_model, report_prompt_switch]

class ReactAgent:

    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=prompt_main_prompt,
            tools=tools,
            middleware=middlewares,
        )

    def execute_stream(self, query):
        input_dict = {
            "messages":[
                {"role": "user", "content": query}
            ]
        }
        resp = self.agent.stream(input=input_dict, stream_mode="values", context={"report": False})

        for chunk in resp:
            latest_msg = chunk['messages'][-1]
            yield latest_msg.content.strip() + "\n"


if __name__ == '__main__':

    agent = ReactAgent()

    # resp = agent.execute_stream("获取当前用户城市的天气数据")
    resp = agent.execute_stream("扫地机器人在我所在的城市的气温下要如何保养")
    resp = agent.execute_stream("扫地机器人在我所在的城市的气温下要如何保养，并且给我输出一个总结报告")
    for chunk in resp:
        print(chunk, end="", flush=True)