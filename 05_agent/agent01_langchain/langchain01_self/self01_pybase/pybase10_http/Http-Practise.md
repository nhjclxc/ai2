# LangChain 之前必须掌握的 HTTP Python 代码练习

这份文档不是讲概念，而是讲：

> 在学习 LangChain 之前，HTTP 相关哪些 Python 代码你必须亲手写过。

如果这些练习没有自己写过，后面学习这些内容时会明显吃力：

* 模型 API 调用
* 第三方工具接入
* 自定义 tool 开发
* SDK 报错排查
* JSON 请求和响应处理

所以这份文档的目标很明确：

> 用最少但足够关键的练习，把 HTTP 基础代码能力补齐。

---

# 学习目标

完成这份练习后，你应该能独立写出：

1. 一个基础 `GET` 请求
2. 一个带 query 参数的请求
3. 一个基础 `POST` JSON 请求
4. 一个带请求头的请求
5. 一个解析 JSON 响应的请求
6. 一个带超时和异常处理的请求
7. 一个基础 API Key 读取与注入示例
8. 一个可复用的 HTTP 请求函数

---

# 练习要求

做这些练习时，建议遵守三个原则：

1. 每个练习单独写成一个 `.py` 文件
2. 每个练习都打印关键结果，不要只写代码不验证
3. 每个练习都要能解释“为什么这么写”

---

# 建议目录结构

建议你在 `self01_pybase/pybase10_http/` 下按下面方式练习：

```text
http01_get.py
http02_query_params.py
http03_post_json.py
http04_headers.py
http05_parse_json.py
http06_timeout_exception.py
http07_api_key_env.py
http08_reusable_client.py
```

你不一定必须用这个命名，但建议保持一题一个文件。

---

# 练习 0：安装 requests

在开始前先确认已安装：

```bash
python -m pip install requests
```

---

## 目标

确保你有最基础的 HTTP 请求库。

---

## 验收标准

你能在 Python 里正常执行：

```python
import requests
print(requests.__version__)
```

---

# 练习 1：最基础的 GET 请求

这是所有 HTTP 练习的起点。

---

## 目标

学会：

* 发一个最简单请求
* 查看状态码
* 查看响应文本

---

## 示例代码

```python
import requests

url = "https://httpbin.org/get"

response = requests.get(url, timeout=10)

print("status_code:", response.status_code)
print("text:")
print(response.text)
```

---

## 你必须理解的点

1. `requests.get()` 是在发 HTTP GET 请求
2. `timeout=10` 不是可有可无，应该形成习惯
3. `response.status_code` 和 `response.text` 是最基本的响应读取方式

---

## 练习要求

自己独立重写一遍，不要直接复制。

然后回答：

1. 为什么要打印状态码
2. 为什么要设置超时
3. 为什么 `response` 不是字符串

---

## 验收标准

你能独立写出一个基础 GET 请求，并解释每一行作用。

---

# 练习 2：带 query 参数的 GET 请求

这一步是为了理解 URL 参数和 `params`。

---

## 目标

学会：

* 传递查询参数
* 理解 query string 是怎么形成的

---

## 示例代码

```python
import requests

url = "https://httpbin.org/get"

params = {
    "q": "langchain",
    "page": 1,
    "lang": "zh"
}

response = requests.get(url, params=params, timeout=10)

print("final_url:", response.url)
print("status_code:", response.status_code)
print(response.json())
```

---

## 你必须理解的点

1. `params` 会被拼接到 URL 上
2. `response.url` 可以帮助你验证最终请求地址
3. query 参数适合简单过滤条件，不适合复杂嵌套对象

---

## 练习要求

改写参数为：

* `keyword=python`
* `sort=latest`
* `limit=5`

然后观察最终 URL。

---

## 验收标准

你能区分：

* query 参数
* body 参数

---

# 练习 3：读取 JSON 响应

HTTP 学习里，JSON 是绝对必须掌握的部分。

---

## 目标

学会：

* 用 `response.json()` 读取 JSON
* 从响应 JSON 中取字段

---

## 示例代码

```python
import requests

response = requests.get("https://httpbin.org/get", timeout=10)
data = response.json()

print(type(data))
print(data.keys())
print(data["url"])
```

---

## 你必须理解的点

1. `response.json()` 返回的是 Python 对象，通常是字典
2. JSON 响应不是普通字符串
3. 读取字段前要知道响应结构

---

## 练习要求

打印以下字段：

* `url`
* `headers`
* `origin`

并解释它们分别表示什么。

---

## 验收标准

你能从 JSON 响应里安全地读取字段，而不是只会 `print(response.text)`。

---

# 练习 4：发送 POST JSON 请求

这是学习模型 API 调用前最关键的一步。

因为现代模型接口绝大多数都基于 POST + JSON。

---

## 目标

学会：

* 使用 `POST`
* 发送 JSON 请求体
* 读取返回结果

---

## 示例代码

```python
import requests

url = "https://httpbin.org/post"

payload = {
    "message": "hello",
    "user": "lxc",
    "tags": ["langchain", "python"]
}

response = requests.post(url, json=payload, timeout=10)

print("status_code:", response.status_code)
print(response.json())
```

---

## 你必须理解的点

1. `json=payload` 会自动把 Python 字典转成 JSON
2. `POST` 常用于发送结构化数据
3. 模型 API 调用的 body 通常也长这样

---

## 练习要求

修改 payload，加入：

* `task`
* `model`
* `temperature`

然后观察响应中服务端回显的数据。

---

## 验收标准

你能自己构造一个 JSON body，并解释为什么这里适合 `POST`。

---

# 练习 5：发送自定义请求头

这一题是为后面的认证和 API key 做准备。

---

## 目标

学会：

* 自定义 headers
* 理解 header 的作用

---

## 示例代码

```python
import requests

url = "https://httpbin.org/headers"

headers = {
    "X-Demo-User": "lxc",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers, timeout=10)

print(response.json())
```

---

## 你必须理解的点

1. header 是附加元信息
2. header 和 body 是不同层
3. 后面 API key 通常也会通过 header 传

---

## 练习要求

给请求增加这些 header：

* `User-Agent`
* `X-Project-Name`

然后查看返回内容。

---

## 验收标准

你能区分：

* header 里放什么
* body 里放什么

---

# 练习 6：发送带 Authorization 的请求头

虽然这里不一定真的调用受保护接口，但你必须先掌握写法。

---

## 目标

学会：

* 构造 Bearer Token 风格请求头
* 理解认证信息的位置

---

## 示例代码

```python
import requests

url = "https://httpbin.org/headers"

headers = {
    "Authorization": "Bearer demo-key-123",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers, timeout=10)

print(response.json())
```

---

## 你必须理解的点

1. 认证信息通常放在 header 中
2. `Bearer xxx` 是常见格式
3. 不要把真实密钥写死在练习代码里

---

## 练习要求

把 token 改成一个变量：

```python
token = "demo-key-456"
```

再拼进 header。

---

## 验收标准

你知道 API key 常见注入位置，也知道不该硬编码真实 key。

---

# 练习 7：从环境变量读取 API Key

这一步是必须会的。

因为后面调用真实模型服务时，不能把 key 写死在源码里。

---

## 目标

学会：

* 从环境变量读取密钥
* 基本判断密钥是否存在

---

## 示例代码

```python
import os

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("OPENAI_API_KEY is missing")
else:
    print("OPENAI_API_KEY loaded")
```

---

## 进阶示例

```python
import os
import requests

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(
    "https://httpbin.org/headers",
    headers=headers,
    timeout=10
)

print(response.json())
```

---

## 你必须理解的点

1. 环境变量是比硬编码更合理的方式
2. 没有 key 时应该明确报错
3. 真实项目里通常先校验配置，再发请求

---

## 验收标准

你能自己写出从环境变量读取 key 的代码，并用于构造 header。

---

# 练习 8：设置超时

这是工程习惯，不是可选项。

---

## 目标

学会：

* 显式设置超时
* 理解没有超时的风险

---

## 示例代码

```python
import requests

response = requests.get("https://httpbin.org/delay/2", timeout=5)
print(response.status_code)
```

---

## 练习要求

尝试把超时改成：

```python
timeout=1
```

观察会发生什么。

---

## 你必须理解的点

1. 请求不一定总能快速返回
2. 没有超时，程序可能长期卡住
3. 超时是实际项目里的基本保护措施

---

## 验收标准

你能解释：

* 什么是超时
* 为什么 HTTP 请求几乎都应该设置超时

---

# 练习 9：捕获请求异常

HTTP 请求基础里，异常处理必须自己写过。

---

## 目标

学会：

* 捕获请求失败
* 打印合理错误信息

---

## 示例代码

```python
import requests

try:
    response = requests.get("https://httpbin.org/delay/3", timeout=1)
    print(response.status_code)
except requests.RequestException as e:
    print("request failed:")
    print(e)
```

---

## 你必须理解的点

1. 网络请求失败是正常情况，不是例外情况
2. `requests.RequestException` 是常见基础捕获入口
3. 错误信息应该被打印或记录，而不是静默吞掉

---

## 练习要求

再做两个实验：

1. 访问一个明显错误的域名
2. 访问一个格式错误的 URL

观察错误信息差异。

---

## 验收标准

你能写出基础异常处理，而不是请求一失败程序就直接崩。

---

# 练习 10：用 `raise_for_status()` 处理非 2xx 响应

这一步非常重要。

很多初学者只判断“有没有 response”，但不会主动处理失败状态。

---

## 目标

学会：

* 把非成功状态码视为错误
* 主动让程序暴露问题

---

## 示例代码

```python
import requests

try:
    response = requests.get("https://httpbin.org/status/404", timeout=10)
    response.raise_for_status()
    print(response.text)
except requests.RequestException as e:
    print("http error:")
    print(e)
```

---

## 你必须理解的点

1. 请求返回不代表业务成功
2. `404`、`500` 这类状态通常应被视为失败
3. `raise_for_status()` 是很实用的基本习惯

---

## 验收标准

你能解释：

* 为什么 `status_code` 为 `404` 时不应该当成正常成功处理

---

# 练习 11：从 JSON 响应中安全取值

后面做工具调用和模型结果处理时，这个能力非常常用。

---

## 目标

学会：

* 从 JSON 里取字段
* 避免直接假设字段一定存在

---

## 示例代码

```python
import requests

response = requests.get("https://httpbin.org/get", timeout=10)
data = response.json()

url = data.get("url")
origin = data.get("origin")
headers = data.get("headers", {})

print("url:", url)
print("origin:", origin)
print("headers keys:", headers.keys())
```

---

## 你必须理解的点

1. 响应字段不一定永远完整
2. `dict.get()` 比直接索引更适合很多容错场景
3. 拿到数据后要先看结构，再消费字段

---

## 验收标准

你能写出一个安全读取 JSON 字段的小脚本。

---

# 练习 12：封装一个可复用的 GET 请求函数

前面的练习都是离散的，这里开始进入“可复用代码”的阶段。

---

## 目标

学会：

* 封装请求逻辑
* 统一超时和异常处理

---

## 示例代码

```python
import requests


def fetch_json(url: str, params: dict | None = None) -> dict:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


data = fetch_json("https://httpbin.org/get", {"q": "langchain"})
print(data["url"])
```

---

## 你必须理解的点

1. 重复逻辑应该提取成函数
2. 函数输入输出要清晰
3. 请求、检查状态、返回 JSON 是一个合理的最小封装单元

---

## 练习要求

给函数补上异常处理：

* 捕获请求异常
* 打印报错
* 返回 `None` 或重新抛出错误

---

## 验收标准

你能把一段散乱请求代码提炼成一个可复用函数。

---

# 练习 13：封装一个可复用的 POST JSON 函数

这是为后续模型调用、工具请求做准备。

---

## 目标

学会：

* 封装 JSON POST 请求
* 统一 header、timeout、错误处理

---

## 示例代码

```python
import requests


def post_json(url: str, payload: dict, headers: dict | None = None) -> dict:
    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=10
    )
    response.raise_for_status()
    return response.json()


result = post_json(
    "https://httpbin.org/post",
    {"message": "hello"}
)

print(result["json"])
```

---

## 练习要求

给这个函数增加：

* 默认 `Content-Type`
* 异常处理
* 对返回 JSON 的基础校验

---

## 验收标准

你能封装一个后续可直接复用到第三方 API 的基础函数。

---

# 练习 14：模拟一个“调用模型 API”的请求结构

这里不一定真的请求某个模型服务，但你必须写过类似结构。

---

## 目标

理解模型调用的典型 JSON body 长什么样。

---

## 示例代码

```python
import requests

url = "https://httpbin.org/post"

payload = {
    "model": "gpt-4.1",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain LangChain briefly."}
    ],
    "temperature": 0
}

headers = {
    "Authorization": "Bearer demo-key",
    "Content-Type": "application/json"
}

response = requests.post(
    url,
    json=payload,
    headers=headers,
    timeout=10
)

print(response.json()["json"])
```

---

## 你必须理解的点

1. 模型请求通常是复杂嵌套 JSON
2. 消息列表会被放在 body 中
3. 认证信息通常放在 header 中
4. 这就是后面 SDK 和 LangChain 底层大致在帮你做的事情

---

## 验收标准

你能看懂并独立写出一个接近真实模型调用结构的 POST 请求。

---

# 练习 15：写一个统一的请求调试输出

这是一个非常实用的习惯。

---

## 目标

学会在调试时打印关键上下文，而不是盲目猜问题。

---

## 示例代码

```python
import requests

url = "https://httpbin.org/get"
params = {"q": "langchain"}

response = requests.get(url, params=params, timeout=10)

print("request url:", response.url)
print("status code:", response.status_code)
print("response headers:", response.headers.get("Content-Type"))
print("response body:")
print(response.text)
```

---

## 你必须理解的点

请求调试时至少要关注：

1. 实际请求地址
2. 状态码
3. 响应格式
4. 返回体

---

## 验收标准

你形成了基本调试习惯，而不是接口一错就只能说“没返回”。

---

# 建议你自己补做的两个小项目

前面是单点练习，下面两个小项目能帮助你把能力串起来。

---

## 小项目 1：天气查询客户端

目标：

* 构造 query 参数
* 发送 GET 请求
* 解析 JSON
* 处理错误情况

即使你先用假接口或模拟接口，这个项目也值得写。

---

## 小项目 2：通用 API 调用器

目标：

* 输入 URL
* 输入方法
* 输入 headers
* 输入 JSON body
* 输出状态码和响应结果

这个练习会显著提升你后面调试第三方 API 的能力。

---

# 完成这些练习后，你应该达到什么水平

完成后，你应该已经具备这些能力：

1. 会写 `GET` 和 `POST`
2. 会传 `params`
3. 会传 `headers`
4. 会发 JSON body
5. 会解析 JSON 响应
6. 会设置超时
7. 会处理请求异常
8. 会读取环境变量中的 API key
9. 会封装基础请求函数
10. 会看请求调试信息

如果这些都能独立写出来，再进入 LangChain 的模型调用、tool 调用和外部服务接入，会顺很多。

---

# 一句话总结

学习 LangChain 之前，HTTP 相关 Python 代码至少要练到这个程度：

```text
会发请求
-> 会带参数和请求头
-> 会解析 JSON
-> 会处理异常和超时
-> 会封装成可复用函数
-> 会看懂接近真实模型调用的请求结构
```

做到这里，HTTP 基础就够支撑后面的 LangChain 学习了。
