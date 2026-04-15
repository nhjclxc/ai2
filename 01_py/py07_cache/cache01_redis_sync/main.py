#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/15 20:34
# Module    : main.py
# explain   :

import redis_sync

cli = redis_sync.RedisClient()

admin = {
    "username": "admin",
    "password": "<PASSWORD>"
}

def kv():
    key = "admin"
    cli.set(key, admin)

    print(f'admin: {cli.get(key)}')

    print(f"exists: {cli.exists(key)}")

    print(f"delete: {cli.delete(key)}")

    print(f"exists 2: {cli.exists(key)}")

# kv()

cli.set("key111", admin, ex=10)

def hash():
    name = "map2"
    key1 = "hash1"
    key2 = "hash2"
    import time
    now_ts = int(time.time())
    cli.hset(name, key1, now_ts)
    cli.hset(name, key2, now_ts + 111)

    print(f'hset[name]: {cli.hget(name, key1)}')
    print(f'hset[name]: {cli.hget(name, key2)}')

    print(f"has exists: {cli.exists(name)}")
    cli.delete(name)
    print(f"has exists 2: {cli.exists(name)}")

# hash()


def list():
    key = "list2"
    lst = [1,2,3,4,5]
    cli.lpush(key, *lst)

    print(cli.rpop(key))
    print(cli.rpop(key))
    print(cli.rpop(key))

    pass

list()


cli.close()
