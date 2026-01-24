#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/10 15:54
# Module    : base12.py
# explain   : 函数，https://docs.python.org/zh-cn/3.10/tutorial/controlflow.html#defining-functions

'''
定义 函数使用关键字 def，后跟函数名与括号内的形参列表。函数语句从下一行开始，并且必须缩进。

1、函数的定义：
def 函数名称(参数列表) -> (返回值类型列表):
    """ 函数的文档docstring """
    函数体
    return 返回值列表


2、函数内变量的作用域：
    函数在 执行 时使用函数局部变量符号表，所有函数变量赋值都存在局部符号表中；引用变量时，首先，在局部符号表里查找变量，然后，是外层函数局部符号表，再是全局符号表，最后是内置名称符号表。
    Local → Enclosing → Global → Builtins
    简单地说就是：先读取函数内部变量，再读取函数外的变量，然后读取全局变量，最后会读取内置变量


3、py传参方式：值传递
    Python 不是“值传递 / 引用传递”，而是“对象引用传递（call by object reference）”

4、函数名可以作为变量把这个函数赋值给其他变量
'''


# 1、函数的定义
def func1(a: int, b: int, s: str) -> tuple[int, str]:
    """
    计算两个整数之和，并生成对应的描述字符串。

    Args:
        a (int): 第一个参与计算的整数
        b (int): 第二个参与计算的整数
        s (str): 描述前缀字符串

    Returns:
        tuple[int, str]:
            - int: a 与 b 的和
            - str: 计算过程的描述字符串，格式为 "{s} :{a} + {b} = {c}"

    Example:
        >>> func1(1, 2, "sum")
        (3, 'sum :1 + 2 = 3')
    """
    c = a + b
    res = f"{s} :{a} + {b} = {c}"
    return c, res


print(func1(1, 2, "这是一个字符串"))


def fib(n: int):
    if n == 0 or n == 1:
        return n
    return fib(n - 1) + fib(n - 2)


print(fib(5))
print(fib(10))

print(" ------------- 2、函数参数参数的作用域 ------------------")
# 2、函数参数参数的作用域
# 2.1、函数内有该变量，则优先读取局部变量
x = 666


def func21():
    x = 123
    print(x)
    x = 222
    print(x)


func21()
print(x)


# 2.2、函数内无局部变量，则读取函数外部变量

def func22_out():
    x22 = 22

    def func22_inner():
        print(x22)

    func22_inner()
    print(x22)


func22_out()

# 2.3、没有外部变量，则读取全局变量，注意：全局变量要使用 global 来声明
# x23被定义为全局变量
x23 = 555


def func23():
    print(x23)


func23()
print(x23)


def func23():
    # 以下演示：无法直接修改 x23 的值
    x23 = 666  # 这个修改只是修改了局部变量x23
    print(x23)  # 输出 666


print(x23)  # 输出 555
func23()
print(x23)  # 输出 555

print("--------------")


def func23():
    # 当在函数内想要修改全局变量时，必须在函数内部使用 global 现在要修改的变量是全局变量

    # 使用global声明x23是全局变量
    global x23
    x23 = 666
    print(x23)  # 输出 666


print(x23)  # 输出 555
func23()
print(x23)  # 输出 666

print("--------------")


# 使用 nonlocal 来内层函数里面修改外层函数的变量
def func25_out():
    x25 = 123
    x25_2 = 465

    def func25_inner():
        # 要修改外部变量时，使用 nonlocal 来声明
        nonlocal x25
        x25, x25_2 = 222, 666
        print(x25, x25_2)

    print(x25, x25_2)
    func25_inner()
    print(x25, x25_2)


func25_out()

"""
在内部函数中：
    nonlocal：绑定并修改外层函数（Enclosing）作用域中的变量
    global：绑定并修改模块级（Global）作用域中的变量
    两者互斥，不能同时用于同一个变量    

简单的说，nonlocal只能指明这个变量是外层函数（最近一层）的变量，不能指明是全部函数的变量
而 global恰恰相反，global只能说明是全局变量，不能指明外层函数的变量
"""
x = 100


def outer():
    x = 10

    def inner_nonlocal():
        nonlocal x
        x += 1
        print("inner_nonlocal x:", x)

    def inner_global():
        global x
        x += 1
        print("inner_global x:", x)

    inner_nonlocal()
    print("outer x:", x)

    inner_global()
    print("outer x:", x)


outer()
print("global x:", x)

print("""Python 不是“值传递 / 引用传递”，而是“对象引用传递（call by object reference）”""")
# 3、py传参方式：值传递
x3 = 123
li3 = [1, 2, 3, 4, 5]
li32 = [1, 2, 3, 4, 5]


def func3(num: int, li: list, li2: list):
    print("func3修改前：", id(num), num)
    print("func3修改前：", id(li), li)
    print("func3修改前：", id(li2), li2)
    num = 666
    li.append(num)  # append 是 原地修改（in-place）
    # 将新的list对象赋值给li2变量，那么li2就放弃了对函数外li32内存地址的引用，而指向了新的对象
    # 因此这一句之后li2再也修改不到实参li32这个list了
    li2 = [5, 6, 7, 8, 9]
    print("func3修改后：", id(num), num)
    print("func3修改后：", id(li), li)
    print("func3修改后：", id(li2), li2)


print("修改前：", id(x3), x3)
print("修改前：", id(li3), li3)
print("修改前：", id(li3), li3)
func3(x3, li3, li32)
print("修改后：", id(x3), x3)
print("修改后：", id(li3), li3)
print("修改后：", id(li32), li32)

print("4、py的函数可以被当成变量使用")


def func4(num) -> int:
    print("输出参数：", num)
    return num * 2


print(func4(1))
print(func4(5))
func4_copy = func4
print(func4_copy(11))
print(func4_copy(55))

print("\n5、函数默认值的使用")

default_str = "hello"


# 注意：如果某个参数给出默认值后，其后面的参数也必须给出默认参数，或者将有默认参数的变量放到后面
# def func5(num1: int, num2: int = 5, str3) -> int: # 默认形参后面跟随非默认形参
# 可以使用变量来给默认值传参
def func5(num1: int, num2: int = 5, str1: str = default_str) -> int:
    # num2默认为5
    res = num1 * num2
    print(f"{default_str} --->>> {res}")
    return res


print(func5(1, 2))
print(func5(1))


# 重要警告： 默认值只计算一次。默认值为列表、字典或类实例等可变对象时，会产生与该规则不同的结果。例如，下面的函数会累积后续调用时传递的参数：
def func52(a: int, L: list = []):
    # 只会给L开辟一次内存空间，后续调用函数都会操作统一空间
    L.append(a)
    return L


print(func52(1))  # [1]
print(func52(2))  # [1, 2]
print(func52(3))  # [1, 2, 3]


# func52 的正确示例
def func52_correct(a: int, L=None):
    if L is None:
        # 每一次调用函数都重新给L开辟空间
        L = []
    L.append(a)
    return L


print(func52_correct(1))  # [1]
print(func52_correct(2))  # [2]
print(func52_correct(3))  # [3]

print("\n6、函数参数的传递方式")
"""
Python 函数参数的传递方式包括：
    位置参数（顺序传参）
    关键字参数
    默认参数
    可变位置参数（*args）
    可变关键字参数（**kwargs）
    仅限位置参数（/）
    仅限关键字参数（*）

注意：位置参数必须在关键字参数之前
    /必须在*前面
"""


def func61(*args):
    # 使用元组来接送参数
    print(args)


func61(1, 2, 3)


def func62(**kwargs):
    # 使用dict来接收参数
    print(kwargs['a'])
    print(kwargs.get("b"))
    print("a" in kwargs)
    print("b" not in kwargs)
    print(kwargs)


func62(a=1, b=2)


def func63(a, b, /, c, d, *, e, f):
    # /之前的必须使用 顺序传参
    # /与*之间的 既可以使用顺序也可以使用关键字
    # *之后的只能使用关键字传参
    print(a, b, c, d, e, f)
    pass


func63(1, 2, d=3, c=8, e=5, f=6)
func63(1, 2, 3, 8, e=5, f=6)
func63(1, 2, 3, 8, f=6, e=5)


# func63(b=1, a=2, 3, 8, f=6, e=5) # 意外实参


def f(
        pos1,
        pos2,
        /,
        default1=1,
        *args,
        kw_only1,
        kw_only2=2,
        **kwargs
):
    # 完整的py传参示例
    pass


# https://docs.python.org/zh-cn/3.10/tutorial/controlflow.html#lambda-expressions
print("\n\n8、py的lambda表达式")
# lambda 关键字用于创建小巧的匿名函数。lambda a, b: a+b 函数返回两个参数的和
# Python 的 lambda 函数只能包含一条表达式，不能写多条语句。
func8 = lambda a, b: a + b
print(func8(1, 2))
print(func8(1, 5))

# lambda结合if判断
a, b = 1, 5
print("a小于b" if a < b else "a大于等于b")

comp = lambda x, y: "x小于y" if x < y else "x大于等于y"
print(comp(1, 2))
print(comp(12, 2))
print(comp(2, 2))

comp2 = lambda x, y: "x>y" if x > y else "x<y" if x < y else "x=y"
print(comp2(2, 2))
print(comp2(1, 2))
print(comp2(2, 1))

# lambda 的应用
