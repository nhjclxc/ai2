# LangChain LLM 学习路线

这份文档只聚焦一个主题：

> 学习 LangChain 里的 LLM 层能力，而不是把 RAG、Agent、LangGraph 全部混在一起。

如果你把 LLM 层学扎实，后面的 Prompt、Tool Calling、RAG、Agent 都会顺很多。  
如果这一层没打牢，后面很容易变成“会拼 demo，不会判断问题出在哪”。

---

# 学习目标

学完这一阶段，你应该具备这些能力：

1. 能正确初始化和调用 LangChain 的聊天模型
2. 能理解 `message -> model -> message` 的核心数据流
3. 能掌握同步、异步、批量、流式调用方式
4. 能做基础 prompt 编排
5. 能拿到结构化输出
6. 能接入 tool calling
7. 能定位常见错误：输出格式错、工具参数错、模型配置错、上下文超限

这份路线不是“背 API”，而是建立 LLM 层的完整心智模型。

---

# 学习范围

这里的 `LLM` 学习范围包括：

* Chat Model
* Message
* Prompt
* Output
* Streaming
* Async
* Tool Calling
* Usage / Cost / Latency
* 错误处理

这里暂时不展开：

* RAG
* Vector Store
* Retriever
* LangGraph
* Agent 系统设计

因为这些都建立在 LLM 层之上。

---

# 总体学习顺序

建议按下面顺序学习：

```text
Python 前置基础
  ↓
LangChain 模型初始化
  ↓
Message 体系
  ↓
Prompt Template
  ↓
模型调用方式
  ↓
输出处理
  ↓
结构化输出
  ↓
Streaming 与 Async
  ↓
Tool Calling
  ↓
调试、成本、稳定性
```

---

# 第一阶段：前置基础

在开始 LangChain LLM 之前，先确保你对下面内容不陌生。

---

## 必须掌握

### 1. Python 基础

至少要会：

* 函数
* 类
* 类型注解
* 字典 / 列表
* 异常处理
* 包导入
* 虚拟环境

---

## 2. API 调用基础

至少理解：

* 什么是请求和响应
* 什么是超时
* 什么是认证密钥
* 什么是 JSON
* 什么是重试

LangChain 本质上还是在帮你组织模型调用链路。

---

## 3. Pydantic 基础

后面做结构化输出时会用到。

至少知道：

* `BaseModel`
* 字段定义
* 校验失败

---

# 第二阶段：理解 LangChain 的 LLM 抽象

这一阶段的目标不是先写复杂代码，而是先理解 LangChain 到底在抽象什么。

---

## 核心心智模型

先记住一句话：

```text
messages -> chat model -> AIMessage
```

LangChain 里现代 LLM 应用的核心，不是“给字符串返回字符串”，而是“消息对象流动”。

---

## 要理解的对象

### 1. Chat Model

例如：

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1")
```

你需要理解：

* 模型实例代表什么
* 参数是如何影响输出的
* 模型对象本身不等于一次调用结果

---

## 2. Message

常见消息类型：

* `SystemMessage`
* `HumanMessage`
* `AIMessage`
* `ToolMessage`

要能回答：

* 为什么现代 LangChain 更强调 message，而不是单纯字符串
* system 消息和 user 消息的职责有什么差别
* tool 返回为什么不是普通字符串

---

## 3. Response

模型返回的不只是文本。

你要开始建立这个意识：

* 返回里有内容
* 有时有工具调用信息
* 有时有 usage 信息
* 有时有 metadata

---

# 第三阶段：模型初始化与基础调用

这一阶段开始正式写代码。

---

## 学习目标

能够独立完成：

* 初始化模型
* 发起一次最简单调用
* 拿到模型返回内容
* 区分字符串输出和消息对象输出

---

## 基础示例

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0
)

response = llm.invoke("请用一句话解释什么是 LangChain")

print(response.content)
```

---

## 必学参数

### 1. `model`

决定底层使用哪个模型。

---

## 2. `temperature`

控制输出随机性。

要知道：

* 低 `temperature` 更稳定
* 高 `temperature` 更发散
* 做结构化任务时通常不宜太高

---

## 3. `max_tokens`

控制输出长度上限。

---

## 4. `timeout`

防止请求无限挂起。

---

## 5. `max_retries`

控制请求失败时的自动重试。

---

## 阶段验收

你应该能解释：

* 为什么 `temperature=0` 常用于信息抽取
* 为什么同样的 prompt 在不同模型上结果不同
* 为什么返回值不是普通字符串而是消息对象

---

# 第四阶段：Message 体系

这是 LangChain LLM 层最容易被低估的部分。

很多后续问题，本质上都和消息组织方式有关。

---

## 学习目标

你应该能手写 message 列表，并理解消息顺序对结果的影响。

---

## 示例

```python
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1")

messages = [
    SystemMessage(content="你是一个严谨的 Python 助手"),
    HumanMessage(content="解释一下列表推导式")
]

response = llm.invoke(messages)
print(response.content)
```

---

## 必学内容

### 1. `SystemMessage`

定义角色、规则、边界。

---

## 2. `HumanMessage`

代表用户输入。

---

## 3. `AIMessage`

代表模型输出。

---

## 4. `ToolMessage`

用于承接工具执行结果。

---

## 关键理解

### 1. 消息顺序很重要

消息不是无序参数，顺序会直接影响模型理解。

---

## 2. 上下文不是“自动记忆”

模型能“记住”前文，本质上是因为你把历史消息又发了一次。

---

## 3. 消息过长会带来成本和噪声

后续做多轮对话时，这会成为重要问题。

---

## 阶段验收

你应该能解释：

* 为什么多轮对话本质上是消息列表累积
* 为什么 system 消息常常比 user 提示更稳定
* 为什么上下文越长不一定越好

---

# 第五阶段：Prompt Template

这一阶段的重点不是“写漂亮 prompt”，而是把 prompt 组织成可复用、可维护的模板。

---

## 学习目标

掌握 LangChain 中最常用的 prompt 组织方式。

---

## 基础示例

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "你是一个翻译助手，请把下面内容翻译成英文：{text}"
)

messages = prompt.invoke({"text": "今天天气很好"})
```

---

## 必学内容

### 1. `ChatPromptTemplate`

最常用。

---

## 2. 模板变量

你需要理解：

* 什么变量由调用方传入
* 什么内容应该写死在模板里

---

## 3. 多消息 prompt

例如把 system 和 human 分开定义，而不是全塞进一个字符串。

---

## 4. Few-shot 基本思想

不是所有任务都要 few-shot，但要知道它什么时候有帮助：

* 需要统一格式
* 需要稳定风格
* 需要建立分类边界

---

## 5. Prompt 与业务边界

一个 prompt 尽量只做一件明确的事。

不要写成：

```text
既要总结
又要翻译
又要分类
还要输出 JSON
```

这类 prompt 稳定性通常很差。

---

## 阶段验收

你应该能独立写出：

* 一个翻译 prompt
* 一个分类 prompt
* 一个结构化抽取 prompt

---

# 第六阶段：模型调用方式

这一阶段是从“会调用”进阶到“知道不同调用接口分别适合什么场景”。

---

## 必学 API

### 1. `invoke()`

单次调用，最常用。

---

## 2. `batch()`

批量处理多个输入。

适合：

* 批量摘要
* 批量分类
* 批量抽取

---

## 3. `stream()`

流式返回。

适合：

* 聊天 UI
* 长文本生成
* 实时展示输出

---

## 4. `ainvoke()`

异步单次调用。

---

## 5. `abatch()`

异步批量调用。

---

## 6. `astream()`

异步流式调用。

---

## 示例：批量调用

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1")

inputs = [
    "解释 Python 装饰器",
    "解释生成器",
    "解释上下文管理器",
]

responses = llm.batch(inputs)

for item in responses:
    print(item.content)
```

---

## 示例：流式调用

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1")

for chunk in llm.stream("写一段简短的自我介绍"):
    print(chunk.content, end="", flush=True)
```

---

## 阶段验收

你应该能说明：

* 什么时候用 `invoke`
* 什么时候用 `batch`
* 什么时候用 `stream`
* 为什么异步接口在高并发场景下更重要

---

# 第七阶段：输出处理

模型输出不应该只停留在 `print(response.content)`。

你需要开始把输出处理当成一层正式能力。

---

## 学习目标

掌握“模型输出如何进入下游程序”。

---

## 必学内容

### 1. 纯文本输出

适合：

* 摘要
* 改写
* 翻译

---

## 2. `StrOutputParser`

理解如何把模型结果整理成稳定字符串。

---

## 3. 输出清洗

例如：

* 去掉多余 markdown
* 去掉解释性前缀
* 去掉模型无关废话

---

## 阶段验收

你应该能把模型结果稳定传给下游函数，而不是只人工看一眼。

---

# 第八阶段：结构化输出

这是 LLM 工程里非常重要的一层。

如果你的目标是做实际应用，这一阶段的重要性通常高于“让模型写得更像人”。

---

## 学习目标

输出稳定、可校验、可消费的结构化结果。

---

## 必学内容

### 1. JSON 输出

让模型尽量输出 JSON。

---

## 2. `JsonOutputParser`

学习如何解析 JSON 格式结果。

---

## 3. Pydantic 结构化输出

例如：

```python
from pydantic import BaseModel

class SummaryResult(BaseModel):
    title: str
    summary: str
    sentiment: str
```

---

## 4. 校验失败处理

你必须开始考虑：

* JSON 不合法怎么办
* 某个字段缺失怎么办
* 字段类型不对怎么办
* 是否需要重试

---

## 示例思路

```text
prompt
  -> llm
  -> parser
  -> pydantic 校验
  -> 失败则重试或报错
```

---

## 阶段验收

你应该能做出一个文本信息抽取器，输出稳定 JSON，而不是一段自然语言描述。

---

# 第九阶段：Streaming 与 Async

这一阶段的重点是性能和用户体验，不只是“API 还能这样调”。

---

## Streaming 必学点

### 1. 为什么要流式

因为：

* 用户能更早看到反馈
* 长文本等待体验更好
* 前端界面更自然

---

## 2. chunk 是增量，不是完整答案

你要理解：

* 流式返回片段
* 需要自己拼接
* 有时 chunk 内容为空或只带 metadata

---

## Async 必学点

### 1. 为什么要异步

因为：

* IO 等待多
* 批量请求时能提高吞吐
* 工具调用和模型调用常常都适合并发

---

## 2. 不要滥用异步

异步不是默认更快，前提是场景真的存在并发收益。

---

## 阶段验收

你应该能：

* 写一个流式打印示例
* 写一个异步批量调用示例
* 解释同步和异步的适用边界

---

# 第十阶段：Tool Calling

这部分虽然常被归到 Agent，但在 LLM 层就应该先学。

因为现代模型调用里，tool calling 已经不是附加功能，而是核心能力之一。

---

## 学习目标

理解模型如何决定调用工具，以及工具结果如何回到模型。

---

## 必学内容

### 1. 工具定义

例如：

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """查询城市天气"""
    return f"{city} 晴，28度"
```

---

## 2. `bind_tools()`

将工具绑定到模型。

---

## 3. 工具调用结果

你需要理解：

* 模型不是直接执行 Python
* 模型是“提出工具调用意图”
* 程序负责真正执行工具
* 工具结果再回传给模型

---

## 4. 参数设计

工具参数应该：

* 明确
* 结构化
* 可校验
* 不要歧义太大

---

## 5. 错误处理

工具可能失败：

* 参数缺失
* 网络错误
* 数据为空
* 权限失败

必须考虑这些分支。

---

## 阶段验收

你应该能独立做出一个：

* 天气查询工具
* 汇率查询工具
* 简单数据库查询工具

并让模型在需要时调用它。

---

# 第十一阶段：成本、延迟与稳定性

很多人学到这里还停留在“能跑”，但工程上真正的问题通常在这里。

---

## 必学内容

### 1. Token 成本意识

要知道：

* prompt 越长越贵
* 历史消息越多越贵
* few-shot 不是免费能力

---

## 2. 延迟意识

要知道：

* 大模型更慢
* 长上下文更慢
* 工具链更长更慢

---

## 3. 稳定性意识

要知道：

* 模型输出不完全可预测
* 结构化输出也可能失败
* 工具调用也可能出错

---

## 4. 重试与超时

至少要有这些策略：

* 请求超时
* 有限重试
* 失败日志
* 明确报错

---

## 5. 观测与调试

你应该养成这种调试习惯：

* 看输入 prompt
* 看消息列表
* 看模型原始输出
* 看 parser 是否失败
* 看工具调用参数

---

## 阶段验收

你应该能定位：

* 是 prompt 不清楚
* 是模型参数不合适
* 是输出解析失败
* 是工具参数有问题
* 是上下文太长

---

# 推荐练习顺序

不要上来就做复杂 Agent。

建议按下面顺序练：

---

## 练习 1：一句话问答

目标：

* 初始化模型
* 调用 `invoke`
* 输出结果

---

## 练习 2：多消息对话

目标：

* 手写 `SystemMessage`
* 手写 `HumanMessage`
* 理解 message 列表

---

## 练习 3：模板化翻译器

目标：

* `ChatPromptTemplate`
* 变量注入

---

## 练习 4：批量摘要器

目标：

* `batch`
* 多输入处理

---

## 练习 5：流式输出 Demo

目标：

* `stream`
* chunk 拼接

---

## 练习 6：结构化抽取器

目标：

* JSON 输出
* Pydantic 校验

---

## 练习 7：工具调用 Demo

目标：

* `@tool`
* `bind_tools`
* 工具返回消息处理

---

## 练习 8：带重试和超时的稳健调用

目标：

* 失败处理
* 日志与调试

---

# 常见误区

---

## 误区 1：把 LLM 学习等同于背模型名

模型名会变，抽象能力和调用方式更重要。

---

## 误区 2：只会 `invoke("xxx")`

如果只会最简单字符串调用，说明还没真正理解 message、prompt、parser、tool。

---

## 误区 3：把输出当成纯文本

实际工程里，很多输出必须是结构化数据。

---

## 误区 4：过早追求 Agent

LLM 层不扎实时，Agent 只会放大问题。

---

## 误区 5：忽略成本与稳定性

能跑一次，不代表系统可用。

---

# 学完这一阶段后再学什么

当你把这份 LLM 路线学完，下一步建议顺序是：

```text
Runnable / LCEL
  ↓
RAG
  ↓
LangSmith
  ↓
LangGraph
  ↓
Agent
```

原因很简单：

* LLM 层解决“怎么调用模型”
* Runnable 解决“怎么组织数据流”
* RAG 解决“怎么接外部知识”
* LangGraph 解决“怎么组织复杂状态工作流”
* Agent 解决“怎么做更高自治的决策系统”

---

# 最终验收标准

如果你完成这份学习路线，应该至少能独立完成下面这几个东西：

1. 一个稳定的聊天模型调用脚本
2. 一个带 PromptTemplate 的翻译或分类小工具
3. 一个支持批量调用和流式输出的示例
4. 一个结构化抽取器
5. 一个简单工具调用 Demo
6. 一个带超时、重试、日志的稳健调用脚本

如果这些都能独立写出来，说明 LangChain 的 LLM 层已经真正入门。

---

# 一句话总结

学习 LangChain 的 LLM，不是先追求复杂，而是先把这一条主线做扎实：

```text
消息怎么组织
-> 模型怎么调用
-> 输出怎么约束
-> 工具怎么接入
-> 问题怎么调试
```

这条线打稳了，后面的所有模块才有意义。
