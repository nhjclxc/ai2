# 学习 LangChain 之前必须掌握的 HTTP 请求基础

这份文档只解决一个问题：

> 在学习 LangChain 之前，HTTP 请求基础至少要学到什么程度？

先给结论：

你不需要先成为网络协议专家，  
但必须理解那些会直接影响模型调用、API 调试、工具开发和错误排查的 HTTP 基础。

如果这些内容不清楚，学习 LangChain 时通常会出现这些问题：

1. 会调用 SDK，但不知道底层到底发生了什么
2. API 报错时，不知道是认证失败、参数错误还是网络超时
3. 会复制 `requests.post(...)`，但不会自己判断请求结构是否正确
4. 做自定义 tool 或第三方接口接入时卡住

所以这份路线图不是讲完整 HTTP 理论，而是讲：

> 学习 LangChain 之前，哪些 HTTP 能力必须掌握。

---

# 学习目标

学完这份内容后，你应该能够：

1. 理解 HTTP 请求和响应的基本结构
2. 知道 `GET`、`POST` 等常见方法的区别
3. 看懂 URL、header、body、query 参数
4. 能用 Python 发送基础 HTTP 请求
5. 能处理 JSON 响应
6. 能看懂常见状态码和报错信息
7. 能理解模型 API 调用和普通 HTTP 请求之间的关系
8. 能为后续 LangChain 的模型调用和工具开发打下基础

---

# 为什么学 LangChain 之前必须懂 HTTP

LangChain 是应用层框架，但它大量能力最终都建立在外部 API 调用之上。

比如：

* 调用 OpenAI 模型
* 调用 embedding 接口
* 请求第三方搜索服务
* 请求天气接口
* 调用内部业务接口

你可以先通过 SDK 间接使用这些能力，  
但如果不懂 HTTP，请求一出问题，你几乎无法定位。

所以这里的目标不是让你手写所有底层请求，而是让你具备：

```text
知道请求发给谁
知道请求带了什么
知道响应返回了什么
知道失败时该看哪里
```

---

# 总体学习顺序

建议按这个顺序学习：

```text
HTTP 是什么
  ↓
请求与响应结构
  ↓
URL 组成
  ↓
常见请求方法
  ↓
Headers
  ↓
Query 参数与 Body
  ↓
JSON 请求与响应
  ↓
状态码
  ↓
超时、重试、异常
  ↓
认证与 API Key
  ↓
用 Python requests 发请求
  ↓
理解 LangChain 和 HTTP 的关系
```

---

# 第一阶段：先建立正确认知

---

## 1. 什么是 HTTP

HTTP 可以先简单理解成：

> 客户端向服务器发请求，服务器返回响应。

在 Python 学习和 LangChain 场景里：

* 你的代码经常是客户端
* 模型服务、搜索服务、天气服务通常是服务器

---

## 2. 什么是 API

API 可以理解为：

> 一个系统对外提供的可调用接口。

HTTP API 就是：

> 通过 HTTP 协议暴露出来的接口。

比如模型服务常见调用方式，本质上就是：

```text
你的程序
-> 发 HTTP 请求
-> 模型服务处理
-> 返回响应
```

---

## 3. 为什么不能只停留在“会调 SDK”

因为 SDK 只是封装层。  
当出现这些问题时，你还是要回到底层概念：

* 参数传错
* 身份认证失败
* 超时
* 网络错误
* 返回格式不符合预期

---

# 第二阶段：理解 HTTP 请求和响应

这是最核心的基础。

---

## 1. 请求是什么

一个 HTTP 请求通常至少包含这些部分：

* 请求方法
* URL
* headers
* body

例如：

```text
POST https://api.example.com/chat
Headers: Authorization, Content-Type
Body: {"message": "hello"}
```

---

## 2. 响应是什么

一个 HTTP 响应通常至少包含：

* 状态码
* headers
* body

例如：

```text
200 OK
Content-Type: application/json
{"answer": "hi"}
```

---

## 3. 你必须建立的心智模型

每次 API 调用，本质上都可以拆成三个问题：

1. 请求发对了吗
2. 服务端是否成功处理了
3. 返回结果是否符合预期

---

## 阶段验收

你应该能说清楚：

* 一个请求至少由哪些部分组成
* 一个响应至少由哪些部分组成

---

# 第三阶段：URL 基础

如果 URL 都看不明白，后面调接口会非常被动。

---

## 1. URL 是什么

URL 就是请求地址。

例如：

```text
https://api.example.com/v1/chat/completions?lang=zh
```

---

## 2. URL 的组成

你至少要看懂：

* 协议：`https`
* 域名：`api.example.com`
* 路径：`/v1/chat/completions`
* 查询参数：`?lang=zh`

---

## 3. 路径参数和查询参数的区别

要知道这两种常见形式：

路径参数：

```text
/users/123
```

查询参数：

```text
/users?id=123
```

---

## 4. 为什么这部分重要

因为后面你要经常判断：

* 请求地址是否写错
* 参数应该放 path、query 还是 body

---

## 阶段验收

你应该能拆解一个 URL，并说清每部分含义。

---

# 第四阶段：常见请求方法

你不需要背所有 HTTP 方法，但以下几个必须熟。

---

## 1. `GET`

通常用于获取数据。

特点：

* 通常没有复杂请求体
* 参数多放在 query 中

例如：

```text
GET /weather?city=beijing
```

---

## 2. `POST`

通常用于提交数据。

特点：

* 常带请求体
* 模型调用接口最常见

例如：

```text
POST /chat/completions
```

---

## 3. `PUT`

通常用于整体更新资源。  
知道基本语义即可。

---

## 4. `DELETE`

通常用于删除资源。  
知道基本语义即可。

---

## 阶段验收

你应该能回答：

* 为什么模型调用接口常用 `POST`
* 为什么查询型接口常见 `GET`

---

# 第五阶段：Headers

HTTP header 是学习 LangChain 前必须懂的一层，因为认证、内容类型、请求跟踪都常靠它。

---

## 1. Header 是什么

可以先把它理解成：

> 附加在请求或响应上的元信息。

---

## 2. 常见请求头

必须认识：

* `Authorization`
* `Content-Type`
* `Accept`

---

## 3. `Authorization`

通常用于身份认证。

例如：

```text
Authorization: Bearer <API_KEY>
```

这在模型 API 调用里非常常见。

---

## 4. `Content-Type`

告诉服务端请求体是什么格式。

最常见的是：

```text
Content-Type: application/json
```

---

## 5. `Accept`

告诉服务端你希望收到什么格式的响应。

---

## 阶段验收

你应该能解释：

* 为什么模型 API 常需要 `Authorization`
* 为什么发送 JSON 时经常要设置 `Content-Type`

---

# 第六阶段：Query 参数和 Body

这是最常见的参数承载方式。

---

## 1. Query 参数

放在 URL 后面，例如：

```text
/search?q=langchain&page=1
```

常用于：

* 搜索
* 过滤
* 分页

---

## 2. Body

放在请求体里。

例如发送 JSON：

```json
{
  "model": "gpt-4.1",
  "messages": [
    {"role": "user", "content": "hello"}
  ]
}
```

---

## 3. 什么时候用 query，什么时候用 body

一般理解：

* 简单查询条件常放 query
* 复杂结构化输入常放 body

模型调用通常是复杂输入，所以大多放在 body。

---

## 阶段验收

你应该能区分：

* 哪些参数适合放 URL
* 哪些参数适合放请求体

---

# 第七阶段：JSON 请求与 JSON 响应

这是必须掌握的核心内容。

因为现代模型 API 和绝大多数第三方接口都高度依赖 JSON。

---

## 1. JSON 是什么

你可以把 JSON 先理解成：

> 一种用来表达结构化数据的文本格式。

---

## 2. 为什么 HTTP 里经常用 JSON

因为它适合表达：

* 对象
* 列表
* 嵌套结构

这和模型消息、工具参数、结构化输出天然匹配。

---

## 3. 你必须掌握的对应关系

Python 里的：

* `dict`
* `list`

经常会和 HTTP 里的 JSON 相互转换。

---

## 4. 常见场景

请求：

```json
{
  "city": "beijing"
}
```

响应：

```json
{
  "temperature": 28,
  "condition": "sunny"
}
```

---

## 5. 必须建立的意识

收到响应后，不是只看“有没有返回文本”，而是要判断：

* 是不是合法 JSON
* 字段是否存在
* 数据类型是否正确

---

## 阶段验收

你应该能：

* 看懂一个 JSON 请求体
* 看懂一个 JSON 响应体
* 知道它如何映射到 Python 的字典和列表

---

# 第八阶段：状态码

状态码是 API 调试的第一层入口。

如果状态码都不看，排错基本靠猜。

---

## 1. `2xx` 成功

最常见：

* `200 OK`
* `201 Created`

表示请求基本成功。

---

## 2. `4xx` 客户端问题

最常见：

* `400 Bad Request`
* `401 Unauthorized`
* `403 Forbidden`
* `404 Not Found`
* `429 Too Many Requests`

这些通常表示：

* 参数错了
* 没认证
* 没权限
* 地址错了
* 请求太频繁

---

## 3. `5xx` 服务端问题

最常见：

* `500 Internal Server Error`
* `502 Bad Gateway`
* `503 Service Unavailable`
* `504 Gateway Timeout`

这通常表示：

* 服务端出问题
* 网关或上游服务出问题
* 服务器临时不可用

---

## 调试习惯

看到请求失败时，先问：

1. 状态码是什么
2. 响应体里有没有错误信息
3. 是我传错了，还是服务端挂了

---

## 阶段验收

你应该能解释：

* `401` 和 `403` 的大致区别
* `404` 一般意味着什么
* `429` 为什么在模型接口中常见

---

# 第九阶段：超时、重试、异常

HTTP 请求不是每次都会成功。

必须提前建立“请求可能失败”的默认认知。

---

## 1. 超时

请求可能因为：

* 网络慢
* 服务端响应慢
* 服务异常卡住

而长时间没有结果。

所以你要理解：

* 为什么要设置超时
* 没有超时可能导致程序卡住

---

## 2. 重试

有些失败适合重试，例如：

* 临时网络波动
* 短暂服务不可用

但有些失败不适合盲目重试，例如：

* API key 错误
* 请求参数错误

---

## 3. 异常

Python 发 HTTP 请求时常见问题包括：

* 连接失败
* 超时
* 返回非预期状态
* JSON 解析失败

---

## 阶段验收

你应该能说清：

* 什么错误适合重试
* 什么错误不应盲目重试

---

# 第十阶段：认证与 API Key

这部分和 LangChain 的模型调用直接相关。

---

## 1. 为什么需要认证

因为很多 API 不是公开匿名使用的。

服务端需要知道：

* 你是谁
* 你是否有权限
* 请求是否应计费

---

## 2. 最常见形式：Bearer Token

例如：

```text
Authorization: Bearer <API_KEY>
```

---

## 3. 为什么不要把密钥硬编码

因为这样会带来：

* 泄露风险
* 不便切换环境
* 不利于部署

推荐通过环境变量读取。

例如：

```python
import os

api_key = os.getenv("OPENAI_API_KEY")
```

---

## 4. 常见错误

* key 缺失
* key 过期
* key 放错 header
* key 前缀格式错误

---

## 阶段验收

你应该能解释：

* 为什么 API key 常放在 header 中
* 为什么不应该写死在源码里

---

# 第十一阶段：用 Python 发送 HTTP 请求

这里建议先学 `requests` 的基础用法。

你不需要一开始就深挖所有高级能力，但必须能独立发出简单请求。

---

## 1. 安装 `requests`

```bash
python -m pip install requests
```

---

## 2. 发送 GET 请求

示例：

```python
import requests

response = requests.get("https://httpbin.org/get", timeout=10)

print(response.status_code)
print(response.text)
```

---

## 3. 带 query 参数的 GET 请求

```python
import requests

params = {"q": "langchain", "page": 1}
response = requests.get(
    "https://httpbin.org/get",
    params=params,
    timeout=10
)

print(response.json())
```

---

## 4. 发送 POST 请求

```python
import requests

payload = {
    "message": "hello"
}

response = requests.post(
    "https://httpbin.org/post",
    json=payload,
    timeout=10
)

print(response.status_code)
print(response.json())
```

---

## 5. 设置 headers

```python
import requests

headers = {
    "Authorization": "Bearer demo-key",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://httpbin.org/post",
    json={"text": "hello"},
    headers=headers,
    timeout=10
)

print(response.json())
```

---

## 6. 读取响应

必须会：

* `response.status_code`
* `response.text`
* `response.json()`
* `response.headers`

---

## 7. 处理异常

```python
import requests

try:
    response = requests.get("https://httpbin.org/get", timeout=10)
    response.raise_for_status()
    data = response.json()
    print(data)
except requests.RequestException as e:
    print(f"request failed: {e}")
```

---

## 阶段验收

你应该能独立写出：

* 一个 `GET` 请求示例
* 一个带 JSON body 的 `POST` 请求示例
* 一个带异常处理的请求示例

---

# 第十二阶段：理解 LangChain 和 HTTP 的关系

这是把前面基础和后续框架学习接起来的关键一步。

---

## 1. LangChain 不是替代 HTTP

LangChain 帮你做的是：

* 模型调用封装
* prompt 组织
* 工具编排
* 输出处理

但很多底层能力仍然依赖：

* HTTP 请求
* 认证
* JSON 序列化
* 网络稳定性

---

## 2. 为什么学了 LangChain 还要会看 HTTP 问题

因为当下面这些问题出现时，根因通常不在“框架抽象层”：

* API key 无效
* 请求超时
* 模型服务限流
* 服务端 500
* 第三方工具接口返回非法 JSON

---

## 3. 未来你会在哪些地方用到这些基础

后续学习中，这些 HTTP 能力会直接用在：

* 配置模型 API
* 理解 SDK 报错
* 写自定义工具
* 接第三方搜索服务
* 接业务系统接口
* 调试 agent 的工具调用链

---

## 阶段验收

你应该能说清：

* LangChain 调模型时，底层为什么仍然离不开 HTTP
* 为什么学习第三方工具接入时必须懂请求和响应结构

---

# 推荐练习顺序

不要只看概念，要自己动手写最小请求示例。

---

## 练习 1：看懂一个 URL

找一个实际接口地址，拆出：

* 协议
* 域名
* 路径
* 查询参数

---

## 练习 2：写一个 GET 请求

目标：

* 发请求
* 读取状态码
* 打印文本响应

---

## 练习 3：写一个带 query 参数的请求

目标：

* 理解 params
* 看服务端回显结果

---

## 练习 4：写一个 POST JSON 请求

目标：

* 理解 body
* 理解 JSON 请求格式

---

## 练习 5：解析 JSON 响应

目标：

* 从 `response.json()` 拿字段
* 判断字段是否存在

---

## 练习 6：加认证头

目标：

* 构造 `Authorization` header
* 理解认证信息的位置

---

## 练习 7：模拟错误处理

尝试：

* 访问错误 URL
* 设置很短超时
* 处理请求异常

---

# 常见误区

---

## 误区 1：觉得学 LangChain 不需要懂 HTTP

这是不现实的。  
框架能帮你封装，但不能替你理解底层错误。

---

## 误区 2：把请求成功等同于业务成功

状态码 `200` 只表示 HTTP 层成功，  
不代表业务返回内容一定正确。

---

## 误区 3：不会区分 header、query、body

这是接口调不通的高频原因。

---

## 误区 4：不设超时

没有超时的请求在实际工程里很危险。

---

## 误区 5：认证信息硬编码

这会导致安全和部署问题。

---

# 是否达到可以开始学 LangChain 的标准

如果你已经能独立做到这些事，就说明 HTTP 基础基本够用：

1. 看懂一个 HTTP 请求的组成
2. 看懂一个 HTTP 响应的组成
3. 区分 `GET` 和 `POST`
4. 理解 URL、query、headers、body
5. 读懂常见状态码
6. 用 Python 发基本请求
7. 解析 JSON 响应
8. 做基础超时和异常处理
9. 理解 API key 的作用和安全做法

做到这些，再进入 LangChain 的模型调用和工具接入，会顺很多。

---

# 一句话总结

学习 LangChain 之前，HTTP 不需要学成“网络工程”，  
但必须学到下面这个程度：

```text
知道请求怎么发
-> 知道响应怎么看
-> 知道错误怎么判
-> 知道认证怎么带
-> 知道 LangChain 底层仍依赖这些机制
```

这就够支撑后续的 LangChain 学习了。
