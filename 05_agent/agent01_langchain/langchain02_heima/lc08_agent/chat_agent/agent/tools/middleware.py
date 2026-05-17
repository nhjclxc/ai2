#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/17 17:11
# Module    : middleware.py
# explain   : agent 使用的中间件定义
from typing import Callable, Awaitable, Any

from langchain.agents import AgentState
from langchain.agents.middleware import before_model, wrap_model_call, dynamic_prompt, ModelRequest, wrap_tool_call
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.runtime import Runtime
from langgraph.types import Command

from langchain02_heima.lc08_agent.chat_agent.utils.file_handler import prompt_main_prompt, prompt_report_prompt
from langchain02_heima.lc08_agent.chat_agent.utils.logger_handler import logger



@wrap_tool_call
def monitor_tool(
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], Awaitable[ToolMessage | Command[Any]]]
    ) -> Awaitable[ToolMessage | Command[Any]] | None:
    """
        包装工具执行装饰器
    :param request: 调用工具前的参数信息构造
    :param handler: 工具执行函数
    :return: 工具执行结果
    """

    try:
        logger.info(f"【工具被调用】 -> {request.tool_call['name']}，args：{request.tool_call['args']}")

        result = handler(request)

        logger.info(f"【工具被调用】 ->  result={result}")

        if request.tool_call['name'] == 'fill_context_for_report':
            request.runtime.context["report"] = True

        return result
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败")

@before_model
def log_before_model(
        state: AgentState, runtime: Runtime
    ):
    """
        模型调用前装饰器
    :param state: 整个agent中的状态记录
    :param runtime: 记录整个执行过程中的执行信息
    :return:
    """

    logger.info(f"即将调用模型：{len(state['messages'])}")


@dynamic_prompt
def report_prompt_switch(request: ModelRequest) -> str:
    """
        生成提示词之前调用此函数
    :param request: 请求数据
    :return: 返回对应的提示词
    """

    report = request.runtime.context["report"]
    logger.info(f"检测是否切换提示词：{report}")
    if report:
        return prompt_report_prompt
    return prompt_main_prompt


