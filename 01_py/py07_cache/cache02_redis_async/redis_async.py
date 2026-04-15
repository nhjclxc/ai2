#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/15 21:06
# Module    : redis_async.py
# explain   :
import redis.asyncio as redis
import json
from typing import Any, Optional


class AsyncRedisClient:
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
    async def close(self):
        await self.client.close()

    # ======================
    # KV
    # ======================
    async def set(self, key: str, value: Any, ex: int = None):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return await self.client.set(key, value, ex=ex)

    async def get(self, key: str) -> Optional[Any]:
        val = await self.client.get(key)
        if val is None:
            return None
        try:
            return json.loads(val)
        except Exception:
            return val

    async def delete(self, key: str):
        return await self.client.delete(key)

    async def exists(self, key: str):
        return await self.client.exists(key)

    # ======================
    # Hash
    # ======================
    async def hset(self, name: str, key: str, value: Any):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return await self.client.hset(name, key, value)

    async def hget(self, name: str, key: str):
        val = await self.client.hget(name, key)
        try:
            return json.loads(val) if val else None
        except Exception:
            return val

    # ======================
    # List
    # ======================
    async def lpush(self, key: str, *values):
        return await self.client.lpush(key, *values)

    async def rpop(self, key: str):
        return await self.client.rpop(key)

    # ======================
    # TTL
    # ======================
    async def expire(self, key: str, seconds: int):
        return await self.client.expire(key, seconds)

    # ======================
    # 分布式锁
    # ======================
    def lock(self, name: str, timeout=10):
        return self.client.lock(name, timeout=timeout)



_redis_client = AsyncRedisClient()


async def get_async_redis():
    return _redis_client