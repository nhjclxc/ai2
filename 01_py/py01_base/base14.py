#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/11 13:59
# Module    : base14.py
# explain   : 错误与异常，https://docs.python.org/zh-cn/3.10/tutorial/errors.html
# 使用 Exception(err msg) 来创建异常信息
# 使用 raise Exception(err msg) 来抛出这个异常信息

"""
在py中
    使用 try 来包裹可能出错的语句
    使用 except 来捕获期望的异常
    使用 else 来执行没有发生异常时要执行的语句
    使用 finally 来确保某些语句一定被执行

try:
    可能出现异常的语句
except 期望的异常1 as e:
    对应的处理1
except 期望的异常2 as e:
    对应的处理2
else:
    没有异常时执行
finally:
    必须执行的语句，入资源的关闭操作

"""


# while，if搭配使用异常
def checkPwd(pwd: str):
    print("当前输入的密码是：", pwd)
    if pwd != "exit":
        raise Exception("密码不正确，请重新输入")
    print("密码输入正确")


flag = False
count = 0
while flag:
    pwd = input("请输入密码：")
    try:
        checkPwd(pwd)
        print("欢迎来到系统！")
        break
    except Exception as e:
        print(e)
        if "密码不正确，请重新输入" in str(e):
            count += 1
    if count == 3:
        print("密码输出错误超过3次，该账户已被锁定！")
        break


# 疑问，当try和finally中都有return时，返回的数据到底是谁返回的
def check_ret_value(flag: bool, num: int) -> str:
    try:
        if num < 0:
            raise Exception("数据小于0")
        return f"try 返回{num}"
    except Exception as e:
        print("捕获异常：", e)
        return f"except 返回{num}"
    finally:
        print("最终被执行的语句")
        if flag:
            return f"finally 返回{num}"


# 通过以下输出，可以得到结论，
# 当finally里面存在return时，无论try或except里面的return返回什么都会被finally里面的return返回的数据给覆盖
# 当finally里面没有return语句时，按照try或except里面return返回的数据返回
print(check_ret_value(True, 1))  # finally 返回1
print()
print(check_ret_value(True, -1))  # finally 返回-1
print()
print()

print(check_ret_value(False, 1))  # try 返回1
print()
print(check_ret_value(False, -1))  # except 返回-1


def div(a: int, b: int) -> float:
    if b == 0:
        raise Exception("除数不能为0")
    return a / b


"""
https://docs.python.org/zh-cn/3.10/tutorial/errors.html#defining-clean-up-actions

如果存在 finally 子句，则 finally 子句是 try 语句结束前执行的最后一项任务。不论 try 语句是否触发异常，都会执行 finally 子句。以下内容介绍了几种比较复杂的触发异常情景：

如果执行 try 子句期间触发了某个异常，则某个 except 子句应处理该异常。如果该异常没有 except 子句处理，在 finally 子句执行后会被重新触发。

except 或 else 子句执行期间也会触发异常。 同样，该异常会在 finally 子句执行之后被重新触发。

如果 finally 子句中包含 break、continue 或 return 等语句，异常将不会被重新引发。

如果执行 try 语句时遇到 break,、continue 或 return 语句，则 finally 子句在执行 break、continue 或 return 语句之前执行。

如果 finally 子句中包含 return 语句，则返回值来自 finally 子句的某个 return 语句的返回值，而不是来自 try 子句的 return 语句的返回值。


"""

print(div(1, 2))

try:
    print(div(1, 0))
except Exception as e:
    if "除数不能为0" in str(e):
        # 只处理自定义异常
        print("捕获到了自定义异常")
    else:
        # 如果不是自定义异常，那么将该异常继续上上层抛出，由上层调用者去处理
        raise e

print(div(1, 1))


# 8.5. 异常链¶， https://docs.python.org/zh-cn/3.10/tutorial/errors.html#exception-chaining
# 如果一个未处理的异常发生在 except 部分内，它将会有被处理的异常附加到它上面，并包括在错误信息中:

# 自定义异常，https://docs.python.org/zh-cn/3.10/tutorial/errors.html#user-defined-exceptions
# 所有用户自定义异常，都应该直接或间接派生自Exception异常
class MyExceptionError(Exception):
    pass

# while使用else
