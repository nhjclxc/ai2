#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/12 20:47
# Module    : base17.py
# explain   : 闭包 和 装饰器

# 闭包是一个特色的函数, 可以保存函数内的一些变量不被销毁
"""
闭包定义:在嵌套函数的前提下,内部函数使用了外部函数所定义发变量,同时外部函数将内部函数作为返回值返回给调用者,那么这个使用了外部函数变量的内部函数就叫做闭包

"""


# 1、闭包
# 使用闭包实现一个计数器

# 外部函数
def counter():
    # 这个count变量不会被释放
    count = 0

    # 内部函数
    def do():
        # 内部函数使用外部函数定义的变量
        nonlocal count
        count += 1
        return count

    # 外部函数将内部函数作为变量返回
    return do


c1 = counter()
print(c1())
print(c1())
print(c1())

c2 = counter()
print(c2())
print(c2())
print(c2())

# 每次调用外函数返回的那个内函数是不同的内存地址,每一次调用外函数都会重新创建一份内函数
print(id(c1))
print(id(c2))
print(id(c1) == id(c2))

print()


# 带参数的闭包函数
def counter2(init_num: int = 0):
    count = init_num

    def do():
        nonlocal count
        count += 1
        return count

    return do


c31 = counter2()
print(c31())
print(c31())
c32 = counter2(8)
print(c32())
print(c32())

print("=" * 10, "装饰器", "=" * 10)

# 2、装饰器
"""
装饰器本质上是一个闭包函数, 装饰器可以让其他函数在不需要做任何代码变动的前提下增加额外功能,装饰器的返回值也是一个函数对象
py的装饰器类似于Java的aop编程

py装饰器有两个特点
    特点1:不修改原程序或函数代码
    特点2:不改变函数或程序调用方法

符合开闭原则

装饰器实现1:标准方式
def wrapper(func):
    def inner(*args, **kwargs):
        # 1.添加在执行原函数之前的操作...
        # 2.执行原函数
        rest = func(*args, **kwargs)
        # 3.添加在执行原函数之后的操作...
        return rest
    return inner

装饰器实现2:语法糖,类似于使用Java里面的注解@符号, 分为两步
# 步骤1:定义装饰器函数(这一步和标准装饰器相同)
def 装饰器函数名称(func):
    def inner(*args, **kwargs):
        # 1.添加在执行原函数之前的操作...
        # 2.执行原函数
        rest = func(*args, **kwargs)
        # 3.添加在执行原函数之后的操作...
        return rest
    return inner
# 步骤2:在原函数上使用装饰器
@装饰器函数名称
def 被装饰的原函数(func):


"""


def register(name: str):
    print("register.1")
    print("register.2")
    print("register.3")
    print("注册成功")
    return f"username-{name}"


print("username = ", register("zhangsan"))


# 现在我要通过装饰器来给 register 添加一个功能,即打印函数入参
# 实现方式1:使用标准版装饰器实现
def wrapper(func):
    def inner(*args, **kwargs):
        # 原函数执行前操作, 参数过滤或重写
        print(f"输出传入注册函数的所有参数: {args}, {kwargs}")

        # 执行原函数, 注意这里的rest是一个返回值元组
        rest = func(*args, **kwargs)

        # 原函数执行后的操作, 如日志记录
        print(f"记录用户执行{func.__name__}函数的日志")

        # 返回原函数的返回值
        return rest

    # 返回闭包函数
    return inner


print("使用装饰器过程")
# 将包装后的函数在此返回给 register 变量,那么这样其他人在调用这个register函数的时候是没感觉的, 不知道这个register函数是否有被包装过
register = wrapper(register)
zs_username = register("zhangsan")
print("zs_username = ", zs_username)


# 标准方式要给每一个函数进行一次wrapper装饰,如果要装饰的函数很多,还是很麻烦,因此使用装饰器实现方式2:语法糖方式实现
# 使用实现装饰器方式2:语法糖

# 要想给以下函数都添加wrapper装饰器,只需要在对应的函数上面加上: @wrapper即可

@wrapper
def login(username: str, password: str):
    print(f"username={username}, password={password} 正在尝试登录")


@wrapper
def send(username: str, msg: str):
    print(f"username={username}, password={msg} 正在发送消息")


login("zhangsan", "123456")
send("zhangsan", "你好世界")


# 3、多个装饰器的执行顺序

# 定义装饰器1
def decorator1(func):
    def do_decorator1(*args, **kwargs):
        print("decorator.1.enter")
        rest = func(*args, **kwargs)
        print("decorator.1.leave")
        return rest

    return do_decorator1


# 定义装饰器2
def decorator2(func):
    def do_decorator2(*args, **kwargs):
        print("decorator.2.enter")
        rest = func(*args, **kwargs)
        print("decorator.2.leave")
        return rest

    return do_decorator2


# 定义装饰器3
def decorator3(func):
    def do_decorator3(*args, **kwargs):
        print("decorator.3.enter")
        rest = func(*args, **kwargs)
        print("decorator.3.leave")
        return rest

    return do_decorator3


# 定义被装饰的函数
@decorator1
@decorator2
@decorator3
def send_msg(name, msg: str = "Hello"):
    res = f"send_msg({name}, {msg})"
    print(res)
    return res


send_msg("zhangsan", "在干嘛？")

print("\n\n")


@decorator3
@decorator2
@decorator1
def send_hello(name, msg: str = "Hello"):
    res = f"send_hello({name}, {msg})"
    print(res)
    return res


send_hello("wangwu", "可以吗？")
"""
decorator.1.enter
decorator.2.enter
decorator.3.enter
send_msg(zhangsan, 在干嘛？)
decorator.3.leave
decorator.2.leave
decorator.1.leave

decorator.3.enter
decorator.2.enter
decorator.1.enter
send_hello(wangwu, 可以吗？)
decorator.1.leave
decorator.2.leave
decorator.3.leave

通过上述输出可以得到结论：如果一个函数存在多个装饰器，那么执行顺序是从上到下（类似于函数递归）
"""
