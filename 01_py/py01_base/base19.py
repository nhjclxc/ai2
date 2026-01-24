#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/15 20:57
# Module    : base19.py
# explain   : 单例模式 和 魔法方法

# __init__：构造函数，初始化对象数据
# __del__：析构函数，当对象的内存空间被释放的时候，由py自动调用这个方法
# __new__：由object基类提供的内置静态方法，作用：在内存中为对象分配内存空间和返回对象的引用地址

# new 和 init 之间的区别：new是类级别的方法，init是实例级别的方法，new先于init被执行

class TestClass(object):

    # __new__ 是静态方法
    def __new__(cls, *args, **kwargs):
        # 用父类来创建这个对象
        # obj = super(TestClass, cls).__new__(cls)
        obj = super().__new__(cls)
        print("1.__new__")
        # 以下返回值是必须返回的，否则当前这个类就无法创建对象
        # # AttributeError: 'NoneType' object has no attribute 'play'
        # tc.play()
        # return object.__new__(cls)

        # 重写__new__的时候一定要返回创建的对象引用地址
        print("super().__new__(cls): ", super().__new__(cls))
        print("obj: ", obj)
        return obj

    def __init__(self):
        print("2.__init__")
        print("self: ", self)

    def __del__(self):
        print("3.__del__")

    def play(self):
        print("play")


tc = TestClass()
print("tc: ", tc)


# 输出顺序：
# 1.__new__，调用父类开辟当前对象的空间，并且都会该引用地址，new里面返回了引用之后该实例对象的self才能使用，否则就是空指针了
# 2.__init__
# 3.__del__


# 1、单例模式
# 单例模式的实现方式：
# 1、通过@classmethod实现
# 2、通过装饰器实现
# 3、通过重写__new__实现
# 4、通过导入模块实现


# 使用 __new__特性实现对象的单例模式
class Singleton(object):
    # 使用 instance 来保存单例对象的引用
    instance = None

    name = "init_name"

    def __new__(cls, *args, **kwargs):
        # 鉴于每次创建对象的时候，都会调用new方法来返回一个新的引用地址
        # 那么能不能在创建的时候判断是否已经被创建过了，如果创建过了就不重新创建了，直接返回原来创建过的地址
        # 在类属性里面使用一个变量来保存对象地址
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance


print(id(Singleton()))
print(id(Singleton()))
print(id(Singleton()))

# 2、魔法方法
# py类的的所有魔法方法：https://docs.python.org/zh-cn/3.10/reference/datamodel.html#basic-customization
