#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/5 17:20
# Module    : f08_查询参数.py
# explain   : 查询参数
# explain   : https://fastapi.org.cn/tutorial/query-params/

import fastapi

app = fastapi.FastAPI()

# 查询参数就是url？后面的key=value参数
# curl "http://127.0.0.1:8001/param?name=zhangsan&age=18"
@app.get("/param")
async def path(name: str, age: int):
    return {"name": name, "age": age}

# 路径参数 + 查询参数
@app.get("/path-param/{item_id}")
async def path_param(item_id: str, name: str):
    return {"item_id": item_id, "name": name}
# C:\Users\nhjcl>curl "http://127.0.0.1:8001/path-param/item123?name=zhangsan"


# bool 参数
@app.get("/param2")
async def param2(flag: bool):
    print(f"flag: {flag}")
    return {"flag": flag}
# C:\Users\nhjcl>curl http://localhost:8001/param2?flag=True
# {"flag":true}
# C:\Users\nhjcl>curl http://localhost:8001/param2?flag=1
# {"flag":true}
# C:\Users\nhjcl>curl http://localhost:8001/param2?flag=on
# {"flag":true}
# C:\Users\nhjcl>curl http://localhost:8001/param2?flag=true
# {"flag":true}
# C:\Users\nhjcl>curl http://localhost:8001/param2?flag=yes
# {"flag":true}


# 多个路径参数
@app.get("/path2/{parg1}/item/{parg2}")
async def path2(parg1: str, parg2: str):


    item = {"parg1": parg1, "parg2": parg2}
    print(f"item: {item}")
    item.update({"union": parg2+parg1})
    item["name"]="asc123"
    print(f"item2: {item}")

    return {"parg1": parg1, "parg2": parg2}
# curl http://localhost:8001/path2/parg111/item/parg222


# 不管是路径参数还是查询参数，如果这个参数是必传的参数，那么这个参数就不能设置默认值


item = {"parg1": "parg1", "parg2": "parg2"}
item |= {"name": "asc123"}

print(f"item2: {item}")