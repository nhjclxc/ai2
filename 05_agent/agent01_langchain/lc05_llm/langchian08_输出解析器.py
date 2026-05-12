#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/5 16:43
# Module    : langchian08_输出解析器.py
# explain   :
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, FewShotPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from lc00_core.model_helper import get_chat_openai


# StrOutputParser
# JsonOutputParser

# 有一个需求，就是当前想将当前模型返回的响应作为一个输入再次传入给模型进行提问
def base_defect_example():

    prompt_template = PromptTemplate.from_template("有一个人她姓：{lastname}，他最近生了一个{gender}孩子，他希望孩子{hope}，请根据这些给孩子取一个名字。注意只要给出名字即可，不要有过多废话。")

    chat = get_chat_openai(streaming=True)

    chain = prompt_template | chat

    resp = chain.invoke(input={"lastname": "张", "gender": "男", "hope": "胸怀大志，有魄力，有担当，有毅力"})
    print(resp.content, type(resp))
    #     <class 'langchain_core.messages.ai.AIMessage'>

# base_defect_example()

# 观察 base_defect_example 方法他只能对模型进行一个提问，无法提问第二次，因此我没希望继续对模型提问，这个时候就要引入解析器
# 我们希望在 prompt_template | chat 之后继续调用模型，注意模型输出的结果是 <class 'langchain_core.messages.ai.AIMessage'>
# 如何将 <class 'langchain_core.messages.ai.AIMessage'> 类型的输入再次输入模型就是当前的问题了

# 1、StrOutputParser
# StrOutputParser 可以将 AIMessage 类型的数据拆解为简单的字符串
# 并且 StrOutputParser 也是Runnable接口的子类实现
# 因此，我们只需要将 StrOutputParser 加入到 chain 中解析第一次model的返回值，并且将 StrOutputParser 的解析结果传入第二次模型即可
# 如：prompt | model1 | parser | model2

def str_parser1():
    prompt_template = PromptTemplate.from_template("有一个人她姓：{lastname}，他最近生了一个{gender}孩子，他希望孩子{hope}，请根据这些给孩子取一个名字。注意只要给出名字即可，不要有过多废话。")

    chat = get_chat_openai(streaming=True)

    str_parser = StrOutputParser(name="字符串解析器")
    print(f"str_parser的名称是：{str_parser.name}")


    chain = prompt_template | chat | str_parser | chat

    resp = chain.invoke(input={"lastname": "张", "gender": "男", "hope": "胸怀大志，有魄力，有担当，有毅力"})
    print(resp.content, type(resp))


# str_parser1()


def str_parser2():
    prompt_template = PromptTemplate.from_template("有一个人她姓：{lastname}，他最近生了一个{gender}孩子，他希望孩子{hope}，请根据这些给孩子取一个名字。注意只要给出名字即可，不要有过多废话。")

    chat = get_chat_openai(streaming=True)

    str_parser = StrOutputParser(name="字符串解析器")
    print(f"str_parser的名称是：{str_parser.name}")

    prompt_template2 = PromptTemplate.from_template("请分析这个名字：{str_parser_name} 所对应的含义")

    # 想要继续给 第二个 chat 模型添加提示词，但是prompt_template2需要的输入是一个dict，而str_parser的输出却是一个字符串
    # 因此这里要借助一个RunnableLambda来实现将前一个输出的字符串转化为后一个输入需要的dict
    # 下面的chain 在 str_parser | prompt_template2这里断开了
    # chain = prompt_template | chat | str_parser | prompt_template2 | chat

    # 加入RunnableLambda
    chain = (
            prompt_template
            | chat
            | str_parser
            # | RunnableLambda(lambda x: {"str_parser_name": x})
            | RunnableLambda(debug_ai_message)
            # | RunnablePassthrough.assign(str_parser_name=lambda x: x)
            | prompt_template2
            | chat
    )

    resp = chain.stream(input={"lastname": "张", "gender": "男", "hope": "胸怀大志，有魄力，有担当，有毅力"})
    for chunk in resp:
        print(chunk.content, end="", flush=True)

def debug_ai_message(x: str) -> dict[str, str]:
    # 在这里可以加入任意的数据处理逻辑
    print(f"debug_ai_message -> {x}")
    return {"str_parser_name": x}

# str_parser2()


# 2、JsonOutputParser
# 注意JsonOutputParser解析器传入的必须要是json字符串否则报错：langchain_core.exceptions.OutputParserException: Invalid json output: xxx...

def json_parser():
    prompt_template = PromptTemplate.from_template("有一个人她姓：{lastname}，他最近生了一个{gender}孩子，他希望孩子{hope}，请根据这些给孩子取一个名字。注意只要给出名字即可，不要有过多废话。注意：返回的数据必须是json格式，只有一对key-value，其中key是parser_name，value是你给我取的名字")

    chat = get_chat_openai(streaming=True)

    json_parser = JsonOutputParser(name="Json 解析器")
    str_parser =StrOutputParser(name="Str 解析器")
    print(f"json_parser 的名称是：{json_parser.name}")

    prompt_template2 = PromptTemplate.from_template("请分析这个名字：{parser_name} 所对应的含义")

    def test():
        input_data = {"lastname": "张", "gender": "男", "hope": "胸怀大志，有魄力，有担当，有毅力"}

        resp1 = (prompt_template | chat).invoke(input=input_data)
        # resp1.content {"parser_name": "张志远"} 这是一个标准的json字符串对象
        print(f"resp1: {resp1.content}")

        resp2 = (prompt_template | chat | json_parser).invoke(input=input_data)
        # resp2 {'parser_name': '张志远'} 这时一个py的dict对象
        print(f"resp2: {resp2}，type：{type(resp2)}")

        # json_parser 的响应数据就会传递给 prompt_template2 作为输入

    test()

    # 加入RunnableLambda
    chain = (
            prompt_template
            | chat
            | json_parser
            | prompt_template2
            | chat
            | str_parser
    )

    resp = chain.stream(input={"lastname": "张", "gender": "男", "hope": "胸怀大志，有魄力，有担当，有毅力"})
    for chunk in resp:
        print(chunk, end="", flush=True) # chain的最后面如果没加 | str_parser 那么使用这个
        # print(chunk.content, end="", flush=True)

    pass

# json_parser()


# 3、RunnableLambda
# 使用 RunnableLambda 将函数加入chain

# 使用 RunnableLambda 来改造 json_parser 对应的实现
def func_parser():

    chat = get_chat_openai(streaming=True)

    chat_prompt_template = ChatPromptTemplate.from_messages([
        ('system', "你是一个精通诗歌的小助手，我要你根据已有诗句得到对应的作者，只要给我作者的名字即可，不要有任何多余的东西。"),
        MessagesPlaceholder(variable_name="historys"),
        ('human', "根据以上示例回答诗歌：{input_shige} 所对应的作者是谁？")
    ])

    historys = [
        ('human', '举头望明月，低头思故乡'),
        ('ai', '李白'),
        ('human', '待到秋来九月八，我花开后百花杀。'),
        ('ai', '黄巢'),
    ]

    chain = (
        RunnableLambda(build_historys_dict)
        | chat_prompt_template
        | chat
    )

    input_shige = "歌女犹唱后庭花"
    resp = chain.stream(input={'historys': historys, 'input_shige': input_shige})
    for chunk in resp:
        print(chunk.content, end="", flush=True)


def build_historys_dict(input: dict) -> dict:
    return {"historys": input.get('historys'), "input_shige": input.get('input_shige')}

# func_parser()

def func_parser2():

    chat = get_chat_openai(streaming=True)

    chat_prompt_template = ChatPromptTemplate.from_messages([
        # ('system', "你是一个精通诗歌的小助手，我要你根据已有诗句得到对应的作者，只要给我作者的名字即可，不要有任何多余的东西。注意：返回的数据必须是json格式，只有一对key-value，其中key是result_name，value就是你给我解析的名字"),
        ('system', "你是一个精通诗歌的小助手，我要你根据已有诗句得到对应的作者，只要给我作者的名字即可，不要有任何多余的东西。"),
        MessagesPlaceholder(variable_name="historys"),
        ('human', "根据以上示例回答诗歌：{input_shige} 所对应的作者是谁？")
    ])

    historys = [
        ('human', '举头望明月，低头思故乡'),
        ('ai', '李白'),
        ('human', '待到秋来九月八，我花开后百花杀。'),
        ('ai', '黄巢'),
    ]

    chat_prompt_template2 = ChatPromptTemplate.from_messages([
        ('human', "根据以上历史消息，给出一个这个作者{parser_name}的一首诗歌？")
    ])

    chain = (
        RunnableLambda(build_historys_dict)
        | chat_prompt_template
        | chat
        | RunnableLambda(func_json_parser)
        | chat_prompt_template2
        | chat
    )

    input_shige = "歌女犹唱后庭花"
    resp = chain.stream(input={'historys': historys, 'input_shige': input_shige})
    for chunk in resp:
        print(chunk.content, end="", flush=True)

    pass

def func_json_parser(x: AIMessage) -> dict[str, str]:
    print(f"json_parser -> {x}")
    # {'parser_name': '杜牧'}
    return {'parser_name': x.content}

# func_parser2()


# 以下实现多阶段对话保留历史消息
# 一个chain链中一直保留历史消息传入下一个对话中
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda

def save_mulit_messages():
    chat = get_chat_openai(streaming=True)

    # Prompt 模板（会吃 history），因此必须手动构造多轮消息的历史数据
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个聊天助手，请基于历史消息进行回答"),
        MessagesPlaceholder(variable_name="historys"),
        ("human", "{input}")
    ])

    # 👉 把新一轮对话加入 history
    def append_history(data: dict):
        historys = data.get("historys", [])
        user_input = data["input"]
        ai_output = data["ai_output"]

        # 每一轮把 (HumanMessage + AIMessage) 追加到 history，再传给下一轮
        new_history = historys + [
            # 这里必须使用 HumanMessage和 AIMessage，不得使用元组('human'/'ai')
            HumanMessage(content=user_input),
            AIMessage(content=ai_output),
        ]

        # 将一个构造好的干净的历史数据返回
        return {
            "historys": new_history
        }

    # 👉 第一步：生成 AI 回复，生成第一步的ai回复
    chain1 = prompt | chat

    # 👉 第二步：把回复写回 history
    chain = (
        # 处理第一次输入的数据，构成一个干净的dict传入下一个chain链
        {
            "historys": lambda x: x.get("historys", []),
            "input": lambda x: x["input"],
        }
        # 将上一个节点输入的所有数据 **x 继续向下传递，
        # "ai_output": chain1.invoke(x).content 将调用一次llm返回第一次llm要解析的数据，并且将这次llm返回的数据和前面输入的数据重写构造一个字典往下传
        | RunnableLambda(lambda x: {
            **x,
            "ai_output": chain1.invoke(x).content
        })
        # 构造历史数据，将这次的输入和这次的llm输出构造一个消息对，追加到已有历史消息中
        | RunnableLambda(append_history)
    )

    # ===== 模拟多轮对话 =====
    data = {"historys": []}

    questions = [
        "你好",
        "你还记得我刚刚说什么吗？",
        "那你再总结一下"
    ]

    for q in questions:
        data["input"] = q
        data = chain.invoke(data)

        print("当前历史：")
        for msg in data["historys"]:
            print(f"{msg.type}: {msg.content}")
        print("-" * 40)


# save_mulit_messages()


# 上上下下左右左右BA

def save_mulit_messages2():

    chat = get_chat_openai(streaming=True)

    chat_prompt_template = ChatPromptTemplate.from_messages([
        ('system', "你是我的一个转化工具，我会给你中文方向词或英文单个字母。情况1：如果我给你‘上下左右’这几个中文那么你就给我返回对应反义词的中文，如给你‘上’返回‘下，给你‘左’返回‘右’。情况2：我会给你‘a,b’这两个字母的小写或者小写，最后你都要返回给我大写的字母，如给你‘a’返回‘A’，给你‘B’返回‘B’。注意你的返回结果里面只能是‘上下左右AB’这几个字或字母，不得返回其他内容"),
        MessagesPlaceholder(variable_name="historys"),
        ('human', "本次给你的输入是：{input_value}")
    ])

    def build_historys(last_data: dict) -> dict:
        historys = last_data.get("historys", [])
        input_value = last_data.get("input_value")
        ai_output = last_data.get("ai_output")

        # print(f"historys -> {len(historys)}")

        historys = historys + [
            HumanMessage(content=input_value),
            AIMessage(content=ai_output),
        ]

        # 返回干净的历史消息记录
        return {
            "historys": historys,
            "last_ai_response": ai_output,
        }

    chain_chat = chat_prompt_template | chat

    chain = (
        {
            "historys": lambda x: x.get("historys", []),
            "input_value": lambda x: x.get("input_value", ""),
        }
        | RunnableLambda(lambda x: {
            **x,
            "ai_output": chain_chat.invoke(x).content
        })
        | RunnableLambda(build_historys)
    )

    history_dict = {}

    inputs = ['下', '下', '上', '上', '右', '左','右', '左', 'b', 'A']

    for i, input in enumerate(inputs):
        history_dict["input_value"] = input
        resp_dict = chain.invoke(input=history_dict)
        print(resp_dict.get("last_ai_response"), end="", flush=True)
        # 核心：将历史记录写回去
        history_dict['historys'] = resp_dict['historys']
        history_dict.setdefault("ai_historys", []).append(resp_dict.get("last_ai_response"))


    print(history_dict.get('ai_historys', []))
    infer_chat_prompt_template_ = ChatPromptTemplate.from_messages([
        ('system', "你是一个从1900年到2000年的一个游戏高手，玩过这期间的很多游戏，请你根据历史记录回答对应的问题。"),
        MessagesPlaceholder(variable_name="historys"),
        ('human', "根据以上ai角色回答的历史记录，注意不是human的输入记录，请你找出可能的游戏是？？？")
    ])


    print("="*20 + " 根据历史数据进行推理阶段 " + "="*20)
    infer_chain = infer_chat_prompt_template_ | chat
    infer_resp = infer_chain.stream(input={"historys": history_dict.get("ai_historys", [])})
    for chunk in infer_resp:
        print(chunk.content, end="", flush=True)


    pass

# save_mulit_messages2()


mydict = {}

print(mydict.get("aa"))
z = mydict.setdefault("aa", "bb")
print(z)
print(mydict.get("aa"))
print("------------")


print(mydict.get("lst"))
zz = mydict.setdefault("lst", [])
print(zz)
zzz = mydict.setdefault("lst", []).append("qaz")
print(zzz)
print(zz)
print(mydict.get("lst"))
mydict.setdefault("lst", []).append("1234567890")
print(mydict.get("lst"))

