#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/29 21:16
# Module    : langchian06_通用提示词模板.py
# explain   :

from langchain02_heima.lc00_core.model_helper import get_chat_openai


# 1、PromptTemplate
# langchian06_通用提示词模板
def prompt_base():
    # 了解 from langchain_core.prompts import ChatPromptTemplate
    # prompt = ChatPromptTemplate.from_template()
    # prompt = ChatPromptTemplate.from_messages([])

    chat = get_chat_openai(streaming=True)

    prompt_template = ChatPromptTemplate.from_template("我是{name}, 今年{age}岁了，来自{city}")

    print("方式1（标准写法）：.format方法进行传参")

    prompt_text = prompt_template.format(name="张三", age=18, city="厦门")
    res = chat.stream(prompt_text)
    for chunk in res:
        print(chunk.content, end="", flush=True)


    print("\n\n\n方式2（基于chain链的写法）：通过.stream 或 .invoke 方法进行传参")

    # langchain 链
    chain = prompt_template | chat

    res2 = chain.stream(input={
        "name": "王五",
        "age": 28,
        "city": "福州",
    })
    for chunk in res2:
        print(chunk.content, end="", flush=True)


    # chain = prompt_text |

# prompt_base()


# FewShotPromptTemplate(
#     examples=使用list添加一些示例数据，list里面嵌套dict,
#     example_prompt=示例数据的提示词模板,
#     prefix=组装提示词，示例数据前内容
#     suffix=组装提示词，示例数据后内容
#     input_variables=列表，要注入的变量列表
# )

# 2、FewShotPromptTemplate
# langchian06_示例提示词模板
def prompt_base_few():

    example_template = PromptTemplate.from_template("单词{word}，对应的反义词是{antonym}")

    examples = [
        {"word": "大", "antonym": "小"},
        {"word": "上", "antonym": "下"}
    ]

    few_shot_prompt = FewShotPromptTemplate(
        example_prompt=example_template,
        examples=examples,
        prefix="给出给定词的反义词，有如下示例：",
        suffix="基于示例告诉我，{input_word}对应的反义词是什么？",
        input_variables=['input_word']
    )

    # 获取模型
    chat = get_chat_openai(streaming=True)

    # 输出构造好的提示词字符串
    prompt_text = few_shot_prompt.invoke(input={"input_word": "左"}).to_string()
    print(prompt_text)
    resp = chat.stream(prompt_text)
    for chunk in resp:
        print(chunk.content, end="", flush=True)


    print("\n" + "="*60 + "\n")
    # 使用 prompt模板对象来构造一个执行链进行调用

    chain = few_shot_prompt | chat
    resp2 = chain.stream(input={"input_word": "前"})
    for chunk in resp2:
        print(chunk.content, end="", flush=True)

    """
给出给定词的反义词，有如下示例：

单词大，对应的反义词是小

单词上，对应的反义词是下

基于示例告诉我，左对应的反义词是什么？
左对应的反义词是**右**。
    """

# prompt_base_few()



def prompt_base_few2():
    # 实现 FewShotPromptTemplate 的使用示例

    example_prompt = PromptTemplate.from_template("国家：{country}, 对应的首都：{caption}")

    examples = [
        {"country": "美国", "caption": "华盛顿"},
        {"country": "加拿大", "caption": "温哥华"},
        {"country": "德国", "caption": "柏林"},
    ]
    few_shot_prompt = FewShotPromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
        prefix="下面我将给你一个国家，你要返回给我这个国家的首都",
        suffix="基于以上示例，请你给出下面国家 {input_country} 的首都。",
        input_variables=['input_country']
    )

    chat = get_chat_openai(streaming=True)

    chain = few_shot_prompt | chat

    resp = chain.stream(input={"input_country": "印度"})

    for chunk in resp:
        print(chunk.content, end="", flush=True)




# prompt_base_few2()


def  prompt_base_few3():
    # 支持多个变量输入

    prompt_template = PromptTemplate.from_template("第一个操作数: {num1}, 操作符：{opt}, 第二个操作数: {num2}, 答案：{answer}")

    examples = [
        {"num1": "2", "opt": "+", "num2": "3", "answer": "5"},
        {"num1": "2", "opt": "*", "num2": "3", "answer": "6"},
        {"num1": "2", "opt": "^", "num2": "3", "answer": "8"},
    ]
    few_shot_prompt = FewShotPromptTemplate(
        example_prompt=prompt_template,
        examples=examples,
        prefix="下面我将给出的操作数和操作符的示例得到最终的计算结果",
        suffix="基于上述示例，请你给出第一个操作数: {input_num1}, 操作符：{input_opt}, 第二个操作数: {input_num2}对应的答案",
        input_variables=['input_num1', 'input_opt', 'input_num2']
    )

    num1 = 2
    opt = "log"
    num2 = 3
    print(few_shot_prompt.invoke({"input_num1": num1, "input_opt": opt, "input_num2": num2}).to_string())

    chat = get_chat_openai(streaming=True)

    chain = few_shot_prompt | chat
    resp = chain.stream(input={"input_num1": num1, "input_opt": opt, "input_num2": num2})
    for chunk in resp:
        print(chunk.content, end="", flush=True)


# prompt_base_few3()
"""
下面我将给出的操作数和操作符的示例得到最终的计算结果

第一个操作数: 2, 操作符：+, 第二个操作数: 3, 答案：5

第一个操作数: 2, 操作符：*, 第二个操作数: 3, 答案：6

第一个操作数: 2, 操作符：^, 第二个操作数: 3, 答案：8

基于上述示例，请你给出第一个操作数: 2, 操作符：log, 第二个操作数: 3对应的答案
我们来分析题目中给出的示例，以确定操作符 `log` 在此上下文中的**含义和运算顺序**。

已知示例：

- `2 + 3 = 5` → 标准加法，左操作数 + 右操作数  
- `2 * 3 = 6` → 标准乘法  
- `2 ^ 3 = 8` → 标准幂运算：**底数^指数 = 2³ = 8**  

注意：`^` 是幂运算，且写为 `base ^ exponent`，即 **第一个操作数是底数，第二个是指数**。

那么对于 `log`，需判断是：
- `log₂(3)`（以第一个操作数 2 为底，第二个操作数 3 为真数）？即 $\log_2 3$  
- 还是 `log₃(2)`（以第二个为底）？  
- 或常用对数/自然对数？但有两个操作数，必为**对数函数的双参数形式**。

在数学和多数编程/计算器约定中：
- `log_b(a)` 表示「以 b 为底，a 的对数」，即 $ \log_b a $，其中 **b 是底数，a 是真数**。
- 在题目中，`log` 是二元操作符，类比 `^`：`2 ^ 3` 明确是 $2^3$，即 **第一个是底、第二个是指数**。  
  那么对称地，`2 log 3` 很可能表示 **以第一个操作数为底、第二个操作数为真数**，即 $\log_2 3$。

✅ 这符合标准数学记号 `log_b a`，也与 `^` 的参数顺序一致（左=底/左=底，右=幂/右=真数）。

因此：
- `2 log 3` = $\log_2 3$

计算其值（精确值无法简化为整数，但可给出精确表达式或近似值）：

$$
\log_2 3 = \frac{\ln 3}{\ln 2} \approx \frac{1.0986122887}{0.69314718056} \approx 1.58496250072
$$

通常保留适当精度，例如 **≈ 1.585**（四舍五入到小数点后3位）。

⚠️ 注意：不能写成整数，也不等于 $\log_{10} 3$ 或 $\ln 3$，因为底数明确是第一个操作数 2。

---

✅ 最终答案：  
**$\log_2 3$（约等于 1.585）**

若题目要求简洁数值答案（如前几个例子给出整数），但此处确实不是整数，故应给出精确表达式或合理近似值。根据示例中均给出**数值结果**（5, 6, 8），本题也应回答数值近似值。

→ **答案：1.585**（四舍五入到小数点后3位）

（注：若要求更高精度，可写 1.58496，但 1.585 是标准三位小数近似）

---

✅ **最终回答：1.585**

"""



from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate
"""

format 和 invoke 方法
    prompt_text = prompt_template.format(name="张三", age=18, city="厦门")
    few_shot_prompt.invoke({"input_num1": num1, "input_opt": opt, "input_num2": num2}).to_string()

"""

from langchain_core.messages import SystemMessage
# 消息占位符 ，必须要使用 invoke 动态注入
from langchain_core.prompts import MessagesPlaceholder


# 3、ChatPromptTemplate
# 支持注入任意数量的聊天历史会话消息
def prompt_chat():

    chat_prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content="你是一个地理小助手，知道每一个国家的首都的地理位置"),
        ('human', "我会给你部分的示例数据，要求你根据示例回答问题"),
        MessagesPlaceholder("historys"),
        ('human', "根据以上历史消息回答以上问题。题目：{input_question}")
    ])

    historys = [
        ('human', "美国"),
        ('ai', "美国的首都华盛顿在美国的东部"),
        ('human', "澳大利亚"),
        ('ai', "澳大利亚的首都堪培拉在澳大利亚的东南部"),
        ('human', "埃及"),
        ('ai', "埃及的首都开罗在埃及的北部"),
    ]

    chat_prompt_val = chat_prompt_template.invoke(input={"historys": historys, "input_question": "印度"})
    print(chat_prompt_val, type(chat_prompt_val))
    print(chat_prompt_val.to_string())

    chat = get_chat_openai(streaming=True)

    resp = chat.stream(input=chat_prompt_val)
    for chunk in resp:
        print(chunk.content, end="", flush=True)
    print()

    chain = chat_prompt_template | chat
    resp2 = chain.invoke(input={"historys": historys, "input_question": "越南"})
    print(resp2.content)


    print()
    # 使用 RunnableLambda 来输出构造好的提示词
    chain = chat_prompt_template | RunnableLambda(debug_prompt) | chat

    chain.invoke({"historys": historys, "input_question": "英国"})

    pass

from langchain_core.runnables import RunnableLambda

def debug_prompt(x):
    print("==== PROMPT ====")
    print(x.to_string())
    return x


prompt_chat()



