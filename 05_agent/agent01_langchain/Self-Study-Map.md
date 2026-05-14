学习 [[LangChain](https://www.langchain.com/?utm_source=chatgpt.com)]([https://www.langchain.com/](https://www.langchain.com/)) 时，建议不要一开始就陷入“几十个模块全学”的状态。

真正重要的是：

> 理解 AI 应用是怎么一步步跑起来的。

---

# 推荐学习路线（非常重要）

建议按这个顺序：

```text
LLM基础
  ↓
Prompt
  ↓
Output Parser
  ↓
Chain / Runnable
  ↓
Memory
  ↓
RAG
  ↓
Tool Calling
  ↓
Agent
  ↓
LangGraph
  ↓
LangSmith
```

这是现在 2026 年最主流的学习路线。

---

# 第一阶段：LLM 基础（最重要）

这是根基。

你需要理解：

* Chat Model
* Message
* temperature
* max_tokens
* system prompt
* tool calling
* streaming

---

## 必学内容

### 1. Chat Model

例如：

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4.1"
)
```

理解：

* invoke()
* stream()
* batch()

---

## 2. Message 类型

LangChain 本质就是：

```text
messages -> model -> messages
```

必须理解：

* SystemMessage
* HumanMessage
* AIMessage
* ToolMessage

---

## 3. Prompt Template

这是 LangChain 最核心之一。

例如：

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "你是一个翻译助手，请翻译：{text}"
)
```

必须掌握：

* 模板变量
* Few-shot
* ChatPromptTemplate

---

# 第二阶段：Runnable（现代 LangChain 核心）

这是现在最重要的部分。

以前是：

```text
LLMChain
SequentialChain
```

现在已经逐渐被 Runnable 体系替代。

---

# 必学 Runnable

## 1. 管道操作符

```python
chain = prompt | llm
```

这是 LangChain 现代写法。

---

## 2. invoke()

```python
chain.invoke({"text": "hello"})
```

---

## 3. batch()

批量执行。

---

## 4. stream()

流式输出。

---

## 5. RunnablePassthrough

你之前已经接触过了。

用于：

* 保留上下文
* 多字段并行
* 数据透传

这是 RAG 和 Agent 高频组件。

---

## 6. RunnableLambda

自定义 Python 逻辑。

例如：

```python
from langchain_core.runnables import RunnableLambda
```

---

## 7. RunnableParallel

并行执行。

这个在：

* 多路检索
* 多 Agent

特别重要。

---

# 第三阶段：Output Parser

这是很多人忽略，但非常重要。

LLM 不稳定。

你必须：

> “把 AI 输出变成结构化数据”

---

# 必学 Parser

## 1. StrOutputParser

最基础。

---

## 2. JsonOutputParser

让模型输出 JSON。

---

## 3. PydanticOutputParser

最重要。

例如：

```python
class User(BaseModel):
    name: str
    age: int
```

这会变成：

```json
{
  "name": "...",
  "age": 18
}
```

这是 AI 工程化核心。

---

# 第四阶段：Memory

现在 Memory 已经不像 2023 年那么热门。

但仍然需要会。

---

# 必学概念

## Conversation History

例如：

```text
用户：我叫张三
AI：你好张三
```

后续能记住。

---

## Message History

现代 LangChain 更推荐：

```python
RunnableWithMessageHistory
```

而不是老版：

```python
ConversationBufferMemory
```

---

# 第五阶段：RAG（最核心实战）

现在 AI 应用里：

RAG 是绝对核心。

---

# RAG 必学内容

## 1. Document Loader

读取：

* PDF
* Word
* Markdown
* Web

---

## 2. Text Splitter

最重要之一。

例如：

```python
RecursiveCharacterTextSplitter
```

理解：

* chunk_size
* overlap

---

## 3. Embedding

例如：

```python
OpenAIEmbeddings
```

理解：

* 向量化
* semantic search

---

## 4. Vector Store

必须会：

* FAISS
* Chroma

生产里：

* Milvus
* pgvector
* Elasticsearch

---

## 5. Retriever

例如：

```python
vectorstore.as_retriever()
```

---

## 6. RAG Chain

现代写法：

```python
retriever | prompt | llm
```

---

# 第六阶段：Tool Calling

2025 后：

Tool Calling 非常重要。

因为：

Agent 本质就是：

```text
LLM + Tools
```

---

# 必学内容

## 1. @tool

例如：

```python
@tool
def get_weather(city: str):
    ...
```

---

## 2. bind_tools()

现代核心 API。

---

## 3. ToolMessage

Agent 内部通信核心。

---

# 第七阶段：Agent（重点）

这是很多人的学习目标。

---

# 必学 Agent

## 1. ReAct Agent

经典 Agent 模式。

```text
Thought
Action
Observation
```

---

## 2. Tool Calling Agent

现在主流。

OpenAI function calling 体系。

---

## 3. AgentExecutor

Agent 运行器。

---

## 4. 多工具协同

例如：

* 搜索
* 数据库
* Shell
* HTTP

---

# 第八阶段：LangGraph（现在非常重要）

2025 之后：

LangGraph 比 LangChain Agent 更重要。

因为：

传统 Agent 不稳定。

---

# 必学内容

## 1. StateGraph

核心。

---

## 2. 节点 Node

每一步任务。

---

## 3. Edge

流程控制。

---

## 4. 条件路由

例如：

```python
if need_tool:
    goto tool
```

---

## 5. Human in the loop

人工介入。

---

## 6. Checkpoint

Agent 持久化。

---

# 第九阶段：LangSmith（生产必学）

生产环境必须会。

---

# 必学内容

## 1. Trace

看 Agent 每一步。

---

## 2. Prompt 调试

---

## 3. Eval

自动评测。

---

## 4. Token 成本分析

---

# 真正重要的能力（核心）

其实真正重要的是：

---

# 1. Prompt Engineering

比框架更重要。

---

# 2. RAG

现在 AI 应用 70% 都是 RAG。

---

# 3. Tool Calling

Agent 核心。

---

# 4. Workflow 思维

这是 LangGraph 核心。

---

# 5. Debug 能力

AI 最大问题：

不是不会写。

而是：

```text
为什么它错了？
```

---

# 不建议深学的旧内容

这些现在很多已经过时：

| 老模块               | 现状  |
| ----------------- | --- |
| LLMChain          | 已弱化 |
| SequentialChain   | 已弱化 |
| ConversationChain | 老旧  |
| MRKL Agent        | 老旧  |
| initialize_agent  | 老旧  |

---

# 现在推荐的现代写法

推荐：

```python
prompt | llm | parser
```

而不是：

```python
LLMChain(...)
```

---

# 推荐实战项目（非常重要）

学 LangChain 最有效的是：

> 一边做项目一边学。

---

# 推荐项目顺序

## 1. AI 翻译器

学习：

* prompt
* output parser

---

## 2. PDF 问答（RAG）

学习：

* embedding
* vector db
* retriever

---

## 3. AI 搜索助手

学习：

* tool calling
* agent

---

## 4. AI 数据分析 Agent

学习：

* Python tool
* code execution

---

## 5. 多 Agent 系统

学习：

* LangGraph
* workflow

---

# 推荐学习资料

## 官方文档（最重要）

* [LangChain Docs](https://python.langchain.com/docs/introduction/?utm_source=chatgpt.com)
* [LangGraph Docs](https://langchain-ai.github.io/langgraph/?utm_source=chatgpt.com)
* [LangSmith Docs](https://docs.smith.langchain.com/?utm_source=chatgpt.com)

---

# 最后给你一个非常重要的建议

不要陷入：

```text
“背 API”
```

真正重要的是：

```text
LLM 怎么思考
数据怎么流动
Agent 怎么决策
```

LangChain 只是工具层。
