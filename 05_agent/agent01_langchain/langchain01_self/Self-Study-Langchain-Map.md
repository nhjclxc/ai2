学习 LangChain，不建议一开始就把“所有模块”都过一遍。

更合理的目标是先建立一条清晰主线：

> 输入是什么，模型怎么调用，数据怎么流动，工具怎么接入，检索怎么增强，系统怎么调试和评测。

LangChain 是应用层编排框架，不是 LLM 学习本身的替代品。  
如果基础概念不清楚，后面学 Agent、LangGraph、RAG 会很容易变成“会抄代码，不会判断设计是否合理”。

---

# 这份路线是否合理

原路线的大方向是对的：

```text
LLM基础 -> Prompt -> Output Parser -> Chain / Runnable -> Memory -> RAG -> Tool Calling -> Agent -> LangGraph -> LangSmith
```

但有几个需要调整的地方：

1. `Memory` 不应该放得过早
2. `RAG` 不能只学“会接向量库”，必须补检索质量、召回策略、评测
3. `Agent` 不应该作为过早重点，很多问题用 Workflow 就够了
4. `LangGraph` 和 `LangSmith` 在现代 LangChain 体系里权重更高，应该更早建立认知
5. 缺少前置能力：模型接口、结构化输出、异常处理、观测与评测

所以更合理的学习顺序是下面这版。

---

# 推荐学习路线（调整后）

建议按这个顺序：

```text
Python与LLM调用基础
  ↓
Prompt 与 Message
  ↓
Structured Output / Output Parser
  ↓
Runnable / LCEL
  ↓
Tool Calling
  ↓
RAG
  ↓
LangSmith
  ↓
LangGraph
  ↓
Memory / Checkpoint / 长会话
  ↓
Agent（作为综合能力，而不是起点）
```

这条路线比“先学 Agent”更稳，因为它符合现代 AI 应用的真实构建顺序。

---

# 学习原则

先记住三条：

1. 先学数据流，再学框架 API
2. 先学可控工作流，再学自治 Agent
3. 先学评测和调试，再追求复杂能力

如果这三条顺序反了，通常会陷入下面的问题：

```text
能跑 demo
不能解释为什么这样设计
出了错不知道卡在哪一层
```

---

# 第一阶段：前置基础

这一阶段不是 LangChain 专属，但必须补。

---

## 必须掌握

### 1. Python 基础

至少要熟悉：

* 函数
* 类
* typing
* dataclass / pydantic
* 异常处理
* 文件读写
* HTTP API 基本概念

如果这些不熟，后面写 tool、parser、state 会非常吃力。

---

## 2. LLM 调用基础

需要理解：

* Chat Model
* messages
* system / user / assistant
* temperature
* max_tokens
* structured output
* tool calling
* streaming
* token usage / cost
* latency

例如：

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1")
```

至少要知道这些调用语义：

* `invoke()`
* `stream()`
* `batch()`
* `ainvoke()`

异步接口很重要，后面做并发检索、并行工具调用时会用到。

---

# 第二阶段：Prompt 与 Message

这一阶段是核心基础，不应该跳过。

LangChain 本质上可以先理解成：

```text
messages -> model -> messages
```

---

## 必学内容

### 1. Message 类型

必须理解：

* `SystemMessage`
* `HumanMessage`
* `AIMessage`
* `ToolMessage`

重点不是背类名，而是理解不同消息在对话协议里承担什么角色。

---

## 2. Prompt Template

例如：

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "你是一个翻译助手，请翻译：{text}"
)
```

必须掌握：

* 模板变量
* 多轮消息模板
* Few-shot
* 部分变量注入
* 如何把检索结果安全地拼进 prompt

---

## 3. Prompt 设计能力

真正重要的是：

* 任务边界写清楚
* 输出格式写清楚
* 失败时的回退策略写清楚
* 不要把多个目标揉进一个 prompt

这是后面所有阶段的基础。

---

# 第三阶段：Structured Output / Output Parser

这部分应该比很多教程强调得更早，因为工程里比“让模型多说一点”更重要的是“让它稳定地产出你能消费的数据”。

---

## 必学内容

### 1. `StrOutputParser`

最基础，用来理解输出后处理。

---

## 2. `JsonOutputParser`

理解 JSON 输出约束，以及模型不守格式时怎么兜底。

---

## 3. Pydantic 结构化输出

例如：

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

必须理解：

* 字段约束
* 校验失败
* 重试策略
* 结构化输出与 tool calling 的区别

这部分是 AI 工程化的分水岭。

---

# 第四阶段：Runnable / LCEL（现代 LangChain 核心）

这部分是 LangChain 现代写法的核心，不建议再把重点放在旧版 `LLMChain` 上。

推荐先建立这个心智模型：

```text
输入对象
  -> prompt
  -> model
  -> parser
  -> 业务后处理
```

---

## 必学内容

### 1. 管道写法

```python
chain = prompt | llm
```

---

## 2. 常用调用方式

* `invoke()`
* `batch()`
* `stream()`
* `ainvoke()`
* `astream()`

---

## 3. 核心 Runnable 组件

必须掌握：

* `RunnableLambda`
* `RunnablePassthrough`
* `RunnableParallel`
* `RunnableBranch`

这些组件决定你是否真的理解“数据是怎么流的”。

---

## 4. 错误处理与重试

至少要知道：

* 哪一层可能报错
* 输出解析失败怎么办
* 外部工具超时怎么办
* 什么时候该重试，什么时候该快速失败

这部分经常被忽略，但实战里非常重要。

---

# 第五阶段：Tool Calling

这是现代 LLM 应用的重要分界点。

很多问题不需要 Agent，只需要：

```text
模型判断是否要调用工具
-> 调工具
-> 把结果回给模型
-> 输出最终答案
```

先把这条链路做稳定，比直接学 Agent 更重要。

---

## 必学内容

### 1. `@tool`

例如：

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    ...
```

---

## 2. `bind_tools()`

这是现代工具接入的核心 API。

---

## 3. `ToolMessage`

要理解它不是普通文本，而是工具调用结果在消息协议中的载体。

---

## 4. 工具设计原则

必须掌握：

* 参数尽量结构化
* 返回值尽量稳定
* 工具职责单一
* 工具失败信息要明确
* 不要把复杂业务逻辑都塞进一个工具

---

# 第六阶段：RAG（最核心实战）

RAG 仍然是最值得投入时间的实战方向之一，但不能只学“切块 + 向量库 + 检索”。

真正要学的是：

```text
知识如何进入系统
如何被切分
如何被召回
如何被重排
如何被引用
如何被评估
```

---

## 必学内容

### 1. Document Loader

常见输入：

* PDF
* Markdown
* Web
* Excel / CSV
* 数据库记录

重点不是“会加载”，而是理解不同文档格式的清洗难度不同。

---

## 2. Text Splitter

例如：

```python
RecursiveCharacterTextSplitter
```

必须理解：

* `chunk_size`
* `chunk_overlap`
* 语义边界
* 标题层级切分
* 不同文档类型需要不同切分策略

---

## 3. Embedding

例如：

```python
OpenAIEmbeddings
```

必须理解：

* 向量化不是“理解全文”，只是映射
* 不同 embedding 模型效果和成本不同
* 查询向量和文档向量的一致性很关键

---

## 4. Vector Store

入门可以先学：

* FAISS
* Chroma

再理解生产常见方案：

* Milvus
* pgvector
* Elasticsearch / OpenSearch

重点是理解索引与检索能力，而不是换库。

---

## 5. Retriever

至少要知道这些差异：

* 相似度检索
* MMR
* 多查询检索
* 混合检索
* 父子文档检索

如果只会 `vectorstore.as_retriever()`，RAG 认知还不够。

---

## 6. Rerank

这是很多学习路线缺失的内容，但在实际效果上非常重要。

需要建立认知：

* 检索负责“召回”
* 重排负责“排序”
* 大量 RAG 问题不是生成错，而是取回来的上下文不对

---

## 7. RAG Chain

现代写法不只是：

```python
retriever | prompt | llm
```

还要考虑：

* 检索结果格式化
* 引用来源
* 无结果时的回退
* 是否允许模型脱离知识库自由发挥

---

## 8. RAG 评测

这是必须补上的内容。

至少要会评估：

* 是否召回到了正确片段
* 回答是否引用了错误上下文
* 回答是否幻觉
* chunk 策略是否影响效果
* top-k 是否合理

不会评测，RAG 就只能靠感觉调。

---

# 第七阶段：LangSmith（尽早接触）

LangSmith 不应该只放在“最后顺手看看”。

更合理的做法是：从你开始写链路和 RAG 的时候，就开始用它观察执行过程。

---

## 必学内容

### 1. Trace

看每一步输入输出。

---

## 2. Prompt 调试

看 prompt 版本差异带来的结果变化。

---

## 3. Eval

至少建立这类意识：

* 有基准样本
* 能批量跑
* 能比较版本
* 能看回归

---

## 4. 成本与延迟分析

必须知道：

* 哪一步最贵
* 哪一步最慢
* 哪一步最不稳定

这会直接影响你后续是否需要引入缓存、并发和更轻量模型。

---

# 第八阶段：LangGraph（现代复杂应用核心）

如果你的目标是做复杂工作流、带状态的多步应用、可中断可恢复的系统，那么 LangGraph 的重要性高于传统 Agent 封装。

---

## 必学内容

### 1. StateGraph

理解“状态”是系统的核心，而不是单次 prompt。

---

## 2. 节点 Node

每个节点做一件清晰的事：

* 分类
* 检索
* 调工具
* 生成
* 审核

---

## 3. Edge 与条件路由

例如：

```text
如果需要查询 -> 去检索节点
如果需要外部数据 -> 去工具节点
如果结果不可信 -> 去审核节点
```

---

## 4. Checkpoint

必须理解持久化状态的意义：

* 长流程恢复
* 多轮会话
* 人工介入后继续执行

---

## 5. Human in the Loop

这是生产系统里非常实用的能力，远比“完全自治”更现实。

---

## 6. 子图与工作流拆分

复杂系统最终都要面对这个问题：

* 哪些步骤做成固定流程
* 哪些步骤交给模型判断
* 哪些步骤必须人工确认

LangGraph 学到这里，才算真正进入工程层。

---

# 第九阶段：Memory / 长会话

这里建议放后面，而不是前面。

原因很简单：

很多初学者把“记忆”理解成神秘能力，但本质上它通常只是：

* 会话历史管理
* 状态持久化
* 用户画像存储
* 长期知识读写

如果前面的消息机制、状态机制、存储机制没搞清楚，Memory 很容易学偏。

---

## 必学内容

### 1. Conversation History

理解历史消息如何影响当前回答。

---

## 2. `RunnableWithMessageHistory`

现代 LangChain 更推荐理解这种方式，而不是只停留在老式 `ConversationBufferMemory`。

---

## 3. 短期记忆 vs 长期记忆

必须区分：

* 短期记忆：本轮或近期对话上下文
* 长期记忆：跨会话保存的用户信息或任务状态

---

## 4. 记忆不等于 RAG

这两个概念经常被混淆，必须分清：

* RAG 解决“外部知识引用”
* Memory 解决“历史状态延续”

---

# 第十阶段：Agent（作为综合能力）

Agent 应该在你掌握前面内容后再重点学。

原因是：

很多所谓 Agent 问题，本质上是以下能力没打牢：

* prompt 约束不清
* 工具设计太差
* 工作流没有边界
* 检索质量不行
* 缺少评测和调试

先把这些做好，再学 Agent，理解会更深。

---

## 必学内容

### 1. ReAct 思想

要理解它的价值，也要理解它的局限：

```text
Thought
Action
Observation
```

局限在于：

* 冗长
* 不稳定
* 难控

---

## 2. Tool Calling Agent

这是现代主流方向，比老式字符串解析 Agent 更实用。

---

## 3. AgentExecutor

理解执行循环、停止条件、工具返回、异常处理。

---

## 4. 什么时候不用 Agent

这点非常重要。

如果问题满足下面任一条件，优先考虑 Workflow：

* 步骤是固定的
* 路由规则可显式表达
* 风险高，需要强控制
* 可解释性比自治性更重要

---

# 不建议深学的旧内容

这些可以知道，但不建议投入太多时间：

| 老模块 | 建议 |
| --- | --- |
| `LLMChain` | 知道即可，重点转向 LCEL |
| `SequentialChain` | 知道即可，重点转向 Runnable 组合 |
| `ConversationChain` | 偏旧 |
| `MRKL Agent` | 偏旧 |
| `initialize_agent` | 偏旧 |

---

# 现代写法心智模型

推荐优先习惯下面这些组合：

```python
prompt | llm | parser
```

```python
inputs -> retriever -> prompt -> llm -> structured output
```

```python
state -> graph node -> conditional edge -> next node
```

不要把重点放在“记住多少 API 名字”，而要放在：

* 输入输出是什么
* 哪一步负责什么
* 哪一层最容易错
* 如何定位问题

---

# 推荐实战项目顺序

学 LangChain 最有效的方法仍然是边做边学，但项目顺序建议调整。

---

## 1. 结构化信息抽取器

目标：

* 输入一段文本
* 输出结构化 JSON

学习重点：

* prompt
* parser
* pydantic
* 错误重试

这是比“AI 翻译器”更好的第一个项目，因为它更工程化。

---

## 2. 多轮对话助手

目标：

* 支持消息历史
* 能追踪上下文

学习重点：

* messages
* history
* streaming

---

## 3. PDF / Markdown 问答系统（RAG）

学习重点：

* loader
* splitter
* embedding
* vector store
* retriever
* 引用来源

---

## 4. 带评测的 RAG 优化项目

目标：

* 同一知识库
* 比较不同 chunk / top-k / rerank 策略

学习重点：

* 检索效果比较
* eval
* LangSmith trace

这一步非常关键，能把“会搭 RAG”升级为“会调 RAG”。

---

## 5. 工具调用助手

目标：

* 查询天气
* 查数据库
* 发 HTTP 请求

学习重点：

* tool schema
* tool calling
* tool error handling

---

## 6. 固定工作流助手（LangGraph）

目标：

* 分类
* 检索
* 审核
* 回复

学习重点：

* state
* routing
* checkpoint
* HITL

---

## 7. Agent 系统

最后再做：

* 搜索 Agent
* 数据分析 Agent
* 多工具协同 Agent

这样更合理，因为此时你已经有足够基础判断 Agent 设计是否必要。

---

# 每个阶段的验收标准

如果没有验收标准，学习很容易停留在“看懂示例”。

---

## 阶段 1 验收

你能解释：

* `temperature` 调高会带来什么
* `system prompt` 和 `user prompt` 的角色差异
* `invoke`、`stream`、`batch` 的使用场景

---

## 阶段 2-4 验收

你能独立写出：

* `prompt | llm | parser`
* 一个结构化输出链
* 一个包含并行或分支的 Runnable 链

---

## 阶段 5-6 验收

你能独立实现：

* 一个稳定工具调用流程
* 一个可解释的 RAG 问答流程
* 一个简单的检索效果对比实验

---

## 阶段 7-10 验收

你能回答：

* 这个问题为什么要用 LangGraph，不是普通 chain
* 这个问题为什么要用 Agent，不是固定 workflow
* 这个系统错在检索、prompt、工具还是状态管理

如果能回答这些，说明不是只会抄代码。

---

# 推荐资料

## 官方资料

* [LangChain Python Docs](https://python.langchain.com/docs/introduction/)
* [LangChain Python API Reference](https://reference.langchain.com/python/langchain/overview)
* [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
* [LangSmith Docs](https://docs.smith.langchain.com/)
* [LangChain GitHub](https://github.com/langchain-ai/langchain)

---

# 最后结论

这份学习路线原本的方向是合理的，但如果按原顺序学习，容易出现两个问题：

1. 过早把注意力放到 Agent，而不是可控工作流
2. 把 RAG 学成“会接库”，却不会做检索质量分析和评测

调整后的版本更适合 2026 年的实际应用开发：

```text
基础调用
-> Prompt / Message
-> 结构化输出
-> Runnable / LCEL
-> Tool Calling
-> RAG
-> LangSmith
-> LangGraph
-> Memory
-> Agent
```

最后记住一句话：

```text
先把可控链路做稳定，再追求复杂自治。
```
