#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/10 20:32
# Module    : base13.py
# explain   : 函数进阶
import builtins
from functools import reduce

# 1、内置函数，https://docs.python.org/zh-cn/3.10/library/functions.html
"""
内置函数

A
abs()
aiter()
all()
any()
anext()
ascii()

B
bin()
bool()
breakpoint()
bytearray()
bytes()

C
callable()
chr()
classmethod()
compile()
complex()

D
delattr()
dict()
dir()
divmod()

E
enumerate()
eval()
exec()

F
filter()
float()
format()
frozenset()

G
getattr()
globals()

H
hasattr()
hash()
help()
hex()

I
id()
input()
int()
isinstance()
issubclass()
iter()
L
len()
list()
locals()

M
map()
max()
memoryview()
min()

N
next()

O
object()
oct()
open()
ord()

P
pow()
print()
property()




R
range()
repr()
reversed()
round()

S
set()
setattr()
slice()
sorted()
staticmethod()
str()
sum()
super()

T
tuple()
type()

V
vars()

Z
zip()

_
__import__()

"""

"""
1️⃣ 类型 / 容器构造 & 查询
len()
list()   tuple()   set()   dict()
str()    int()     float() bool()


2️⃣ 迭代 & 序列处理
range()
enumerate()
zip()

3️⃣ 输出 & 调试
print()
type()
id()

4️⃣ 条件判断 / 真值测试
any()
all()

5️⃣ 高阶函数（函数式核心）
map()
filter()
sorted()

6️⃣ 查找 / 反射 / 动态性
getattr()
setattr()
hasattr()

7️⃣ 类型与继承判断
isinstance()
issubclass()

8️⃣ 迭代器协议
iter()
next()

9️⃣ 对象模型 / 元编程
type()
super()
property()
classmethod()
staticmethod()

🔟 命名空间 & 运行环境
globals()
locals()
vars()
__import__()



"""

# 查看所有内置函数
print(dir(builtins))

# 1.1、zip函数：将可迭代对象作为参数，将对象对应的元素打包成中一个个元组，返回一个可迭代对象
# 注意：由于zip()函数返回的是一个可迭代对象，因此zip返回的对象只能访问一次，要想多次访问可以先转化为list后进行多次访问。【py的迭代器是惰性的，】
# 多个可迭代对象进行打包的时候，打包后的数据长度，取决于打包前所有可迭代对象中长度最小的那个长度
li = [1, 2, 3, 4, 5, 6]
lis = ["a", "b", "c", "d", "e"]
print(type(li), li)
li_zip = zip(li, lis)
print(type(li_zip), li_zip)
# zip对象不能使用下标访问
# 访问方式1：遍历打包后的元组
for item in li_zip:
    print(item, item[0], item[1])

# 访问方式2：将zip对象转化为list进行下标访问
# zip_list = list(li_zip)
zip_list = list(zip(li, lis))
print(zip_list, type(zip_list))
print(zip_list[0])

# 1.2、map(): 对可迭代对象中的每一个元素进行一次映射操作，返回一个可迭代对象
# map(func, iter)
li12 = [1, 2, 3, 4, 5]
li12_m = map(lambda ele: f"{ele}-{chr(96 + ele)}", li12)
print(type(li12_m), li12_m)
for item in li12_m:
    print(item)

# 如果映射函数复制时，要单独使用def定义一个函数

# 1.3、reduce()：对参数序列中的元素进行累加操作
li13 = [1, 2, 3, 4, 5]
# reduce函数的第一个参数是：二元执行函数，第二个参数是：可迭代对象，累加的初始值
# 当reduce有第三个初始值参数时，执行函数第一次执行到x的时候x是初始值5，y是可迭代对象的第一个值。后学则x是上一次的计算结果，y则是下一个要计算的元素
print(reduce(lambda x, y: x + y, li13, 5))
# 5,1, 5+1=6
# 6,2, 6+2=8
# 8,3, 8+3=11
# 11,4, 11+4=15
# 15,5, 15+5=20

# 当reduce没有第三个初始值参数时，执行函数第一次的x是可迭代对象的第一个值，y是可迭代对象的第二个值，后续则是x是上一次的计算结果，y是下一个要计算的元素
print(reduce(lambda x, y: x + y, li13))
# 1,2, 1+2=3
# 3,3, 3+3=6
# 6,4,  6+4=10
# 10,5, 19+5=15

# 1.5、enumerate, 给循环“自动加索引”,把一个可迭代对象，变成 (索引, 元素) 的迭代器。
# enumerate本质上使用的是：zip(range(...), iterable)
print("\n1.5、enumerate")
li5 = [1, 2, 3, 4, 5]
for item in li5:
    print(item)
# TypeError: cannot unpack non-iterable int object
# for x, y in li5:
# 以上可知，使用for in循环只能得到一个返回值，即元素数据，如果想要索引的话，那么无法得到
# 因此这时候就可以使用enumerate函数来包装以下li5对象，使得for in遍历的时候可以得到(索引, 数据)这样的一对元组
for index, item in enumerate(li5):
    print(index, item)

# 注意：enumerate返回的是迭代器，只能访问一次，要想多次访问可以转化为list
li5e = enumerate(li5)
print("第一次访问li5e")
for index, item in li5e:
    print("一：", index, item)
print("第二次访问li5e")
for index, item in li5e:
    print("二：", index, item)
li5eli = list(enumerate(li5))
print("第一次访问li5eli")
for index, item in li5eli:
    print("一li5eli：", index, item)
print("第二次访问li5eli")
for index, item in li5eli:
    print("二li5eli：", index, item)

# 1.6、sorted：返回新列表的排序，对任意可迭代对象排序，返回新 list
# soeted返回列表的升序序列
# sorted() 不修改原对象
# list.sort() 会修改原列表并返回 None
print("\n1.6、sorted")
li6 = [1, 8, 2, 9, 3, 0, 4, 6, 5]
print(sorted(li6))
print(sorted(li6, reverse=True))

# 当要排序的是列表存储的是dict或对象时，可以使用sorted里面的key参数来指定排序的属性
students = [
    {"name": "s1", "score": 78},
    {"name": "s2", "score": 65},
    {"name": "s3", "score": 99},
    {"name": "s4", "score": 90},
    {"name": "s5", "score": 51},
]
print(students)
# 要求按照score的升序排序
s2 = sorted(students, key=lambda s: s["score"])
print(s2)

# 1.7、filter，按条件筛选元素，根据函数返回值的真假，过滤元素， 返回一个可迭代对象
# 不修改原对象，会返回一个修改过后的新对象

print("\n1.7、filter")
li7 = [1, 8, 2, 9, 3, 0, 4, 6, 5]
print("li7", li7)
li7_filtered = filter(lambda i: i % 2 == 1, li7)
print("li7_filtered", list(li7_filtered))
# 实战中常被列表推导替代
li7_filtered2 = [item for item in li7 if item % 2 == 1]
print("li7_filtered2", li7_filtered2)

# 1.8、any,有一个为真就 True,只要 iterable 中 有一个真值，就返回 True
# ang表示可迭代对象中任意一个元素为真，即返回真
li8 = [0, 0, 0, 0, 0, 0]
print(any(li8))
li82 = [0, 1, 0, 0, 0, 0]
print(any(li82))
li83 = [0, 1, 0, -1, 0, 0]
print(any([x < 0 for x in li83]))

# 1.9、all,全部为真才 True,iterable 中 所有元素都是真值 才返回 True


# 拆包：对于函数中的多个返回数据，去掉元组，列表或者字典，直接获取里面数据的过程
# 拆包：简单地说就是将元组，列表或者字典里面指定该的数据放到一个变量里面的过程
print("\n拆包")
tp = (1, 2, 3)
# 每一次通过索引来访问tp很繁琐，因此就需要拆包
print(tp[0], tp[1], tp[2])

# 拆包方法1：有多少个元素就定义多少个变量来接收，如果元素太多，那么这种方式就不适合了
# 要求接收变量个数必须和元组内元素的个数相同
# a, b = tp  # 值太多，无法解包 ValueError: too many values to unpack (expected 2)
a, b, c = tp
print(a, b, c)

# 方法2：*接收参数
a2, *b2 = tp
print(a2, "---", *b2, " === ", b2, type(b2))
c2, d2 = b2
print(c2, d2)
