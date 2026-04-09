


# 可以为 FastAPI 应用程序添加中间件。
# fastapi的中间件类似于 SpringBoot 的拦截器

"""

“中间件”是一个在任何特定路径操作处理之前，与每个请求协同工作的函数。同时，它也是在返回每个响应之前与之协同工作的函数。
    它接收进入应用程序的每个请求。
    然后它可以对该请求执行某些操作或运行任何必要的代码。
    然后它将请求传递给应用程序的其余部分（由某个路径操作）进行处理。
    然后它接收应用程序（由某个路径操作）生成的响应。
    然后它可以对该响应执行某些操作或运行任何必要的代码。
    然后它返回响应。
"""
import time

from fastapi import FastAPI, Request
from pygments.lexer import default

app = FastAPI()

"""
您需要在函数上方使用装饰器 @app.middleware("http")。

中间件函数接收
    1、request。
    2、一个名为 call_next 的函数，它将接收 request 作为参数。
        此函数会将 request 传递给相应的路径操作。
        然后它返回相应路径操作生成的 response。
    3、然后您可以进一步修改 response，然后再返回它。
"""
@app.middleware("http")
async def fastapi_interceptor(request: Request, call_next):
    # 不能修改 headers，使用 state 传递 token
    request.state.token = "<PASSWORD>"
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/f23/getInfo")
async def get_info(request: Request):
    print("get info: ", request.state.token)
    pass



