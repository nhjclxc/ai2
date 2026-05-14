#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/15 20:25
# Module    : redis_sync.py
# explain   :

# uv add redis

import redis
import json
from typing import Any, Optional


# localhost, 6379, root, ,
class RedisClient:
    def __init__(
        self,
        host="localhost",
        port=6379,
        db=0,
        password=None,
        max_connections=10,
    ):
        self.pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            max_connections=max_connections,
            decode_responses=True,
        )
        self.client = redis.Redis(connection_pool=self.pool)

    # ======================
    # 关闭
    # ======================
    def close(self):
        self.client.close()

    # ======================
    # 基础 KV
    # ======================
    def set(self, key: str, value: Any, ex: int = None):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return self.client.set(key, value, ex=ex)

    def get(self, key: str) -> Optional[Any]:
        val = self.client.get(key)
        if val is None:
            return None
        try:
            return json.loads(val)
        except Exception:
            return val

    def delete(self, key: str):
        return self.client.delete(key)

    def exists(self, key: str) -> bool:
        return self.client.exists(key) == 1

    # ======================
    # Hash
    # ======================
    def hset(self, name: str, key: str, value: Any):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return self.client.hset(name, key, value)

    def hget(self, name: str, key: str):
        val = self.client.hget(name, key)
        try:
            return json.loads(val) if val else None
        except Exception:
            return val

    # ======================
    # List
    # ======================
    def lpush(self, key: str, *values):
        return self.client.lpush(key, *values)

    def rpop(self, key: str):
        """ 移除最旧的一个数据 """
        return self.client.rpop(key)

    def lrange(self, key: str, start: int = 0, end: int = -1):
        """ 读取数据而不删除 """
        return self.client.lrange(key, start, end)

    # ======================
    # TTL
    # ======================
    def expire(self, key: str, seconds: int):
        return self.client.expire(key, seconds)

    # ======================
    # 分布式锁
    # ======================
    def acquire_lock(self, name: str, timeout=10):
        return self.client.lock(name, timeout=timeout)



if __name__ == '__main__':

    redis_client = RedisClient()

    redis_client.set("langchain_redis", "welcome langchain")
    print(redis_client.get("langchain_redis"))

    redis_client.lpush("langchain_redis_list", "v1")
    redis_client.lpush("langchain_redis_list", "v2")
    redis_client.lpush("langchain_redis_list", "v3")
    redis_client.lpush("langchain_redis_list", "v4")
    redis_client.lpush("langchain_redis_list", "v5")
    redis_client.lpush("langchain_redis_list", "v6")

    pop_val = redis_client.rpop("langchain_redis_list")
    print("popval = ", pop_val)

    list_val = redis_client.lrange("langchain_redis_list")
    print(list_val, type(list_val))

    pass