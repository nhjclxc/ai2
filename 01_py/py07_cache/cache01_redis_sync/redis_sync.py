#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/15 20:25
# Module    : redis_sync.py
# explain   :

# pip install redis

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
        return self.client.rpop(key)

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
