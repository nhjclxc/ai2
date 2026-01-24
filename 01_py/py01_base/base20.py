#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/15 20:57
# Module    : base19.py
# explain   : 迭代器、生成器， https://docs.python.org/zh-cn/3.10/tutorial/classes.html#iterators

# 1、迭代器
# 可迭代对象必须实现以下两个方法：__iter__和__next__
class MyList(object):
    def __init__(self, data=None):
        super().__init__()
        if data is None:
            data = []
        self.data = data
        # 保存当前被访问的索引，当 self.index == len(data) - 1时，表示当前对象已被全部访问完毕
        # 全部访问完毕之后，不得在进行访问，因为迭代器对象只能被访问一次
        self.index = 0

    # 实现迭代器方法1 __iter__，这个方法将可迭代对象本身返回，即返回当前对象的引用，即self
    def __iter__(self):
        return self

    # 实现迭代器方法2 __next__，这个方法返回当前被访问的元素
    def __next__(self):
        if self.index == len(self.data):
            raise StopIteration
        self.index += 1
        return self.data[self.index - 1]

    # len(mlist2)
    def __len__(self):
        return len(self.data)

    pass


lis = [1, 2, 3, 4, 5, 6, 7, 8, 9]
mlist = MyList(lis)
for i in mlist:
    print(i)

mlist2 = MyList(lis)
for i in range(0, len(mlist2)):
    print(next(mlist2), end="," if i != len(mlist2) - 1 else "\n")
    # print(mlist2.__next__(), end="," if i != len(mlist2) - 1 else "\n")

# 判断一个对象是不是可迭代对象，使用 isinstance(mlist, Iterable)
from collections.abc import Iterable

print(isinstance(mlist, Iterable))
print(isinstance("mlist", Iterable))
print(isinstance([1, 2, 3], Iterable))
print(isinstance(123, Iterable))

print("--------------------- 2、生成器 ------------------------")


# https://docs.python.org/zh-cn/3.10/tutorial/classes.html#generators
# 2、生成器，一遍循环一遍计算的机制
# 使用了yield的函数被称为是生成器函数, 生成器函数是惰性函数
# 使用生成器实现斐波那契数列: 0，1，1，2，3，5，8，13，21，34，55，89
# f(n) = f(n-1)+f(n-2)
def fib(n):
    a, b = 0, 1
    for i in range(n):
        yield a
        a, b = b, a + b


# 调用该 fib(10) 只是返回一个生成器函数，并不能把所有的数据都返回，生成器函数是惰性函数
# 要想返回每一个数据，必须要多次调用，即要一个数据就调用一次，
# 生成器函数的数据必须要通过next方法或者for遍历的形式来获取
fib1 = fib(10)
print("next: ", next(fib1))
print("next: ", next(fib1))
print("next: ", next(fib1))
for f in fib1:
    print(f)
