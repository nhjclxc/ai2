#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/5 14:43
# Module    : f01.py
# explain   : python 类型介绍
# explain   : https://fastapi.org.cn/python-types/#pydantic-models
from pydantic import BaseModel


def get_full_name(name: str = "zhangsan", age: int = 20):

    res = f"Name: {name.title()}, Age: {age}"

    sss = name.capitalize() + " is this old " + str(age)

    print(sss)

    return res


print(get_full_name("zhangsan", 18))

# 声明一个带有类型的list
# []中的类型称为类型参数
# 这意味着变量 item是一个list，并且这个list里面存储的是str类型的数据
def process_items(items: list[str]):
    for item in items:
        print(item)



def process_items2(items_t: tuple[int, int, str], items_s: set[bytes]):
    return items_t, items_s

def process_items3(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)

# 使用联合 Union，来声明一个变量支持的多个类型
# 直接使用Union来声明一个变量的话，它不支持None的参数
# def process_item(item: Union[int, str]):
# 使用 Optional 来进一步的表示item参数不仅支持 int 和 str，并且还支持None参数
# def process_item(item: Optional[int, str]):
# py310+可以简单的使用以下方式
def process_item(item: int | str = None):
    print(item)

# 应为类型 'int | str'，但实际为 'None'
process_item(None)

# 使用类 作为一个参数类型
class Person(BaseModel):
    name: str
    age: int
    address: str = "上海外滩"
    friends: list[int] = []


# 某个类（Person）如果继承了 BaseModel 的话，要想创建一个对象，那么必须使用关键字传参
# 或者使用dict传参，即**kwargs

def get_person(per: Person = None):

    if per is None:
        per = Person(name="张三", age=18)
    print(per)

get_person()
get_person(Person(name="kisi", age=15, address="北京"))

per_dict = {
    "name": "wnagwu",
    "age": 28,
    "friends": [1,2,3],
}
get_person(Person(**per_dict))