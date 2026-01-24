#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/1/11 17:29
# Module    : base.py
# explain   : 标准输入输出,https://docs.python.org/zh-cn/3.10/tutorial/inputoutput.html
# 文件读写

# 读写文件的基本操作
# 1.打开文件
f = open('base16.txt', 'r+', encoding="utf-8")
# 2.读写文件
print(f.readline())
# 3.关闭文件
f.close()

# 当open某个不存在的文件时,会抛出如下异常
# FileNotFoundError: [Errno 2] No such file or directory: 'base162.txt'
# open('base162.txt', 'r+', encoding="utf-8")

# 此时就需要捕获改异常,防止程序奔溃
f2 = None
try:
    f2 = open('base162.txt', 'r+', encoding="utf-8")
except FileNotFoundError:
    print("打开失败,没有找到指定的文件")
finally:
    if f2:
        f2.close()

# 以上方法可以使用,要先定义一个变量,并且要在finally里面关闭,很繁琐
# py提供了更好用的方法, with, 不需要手动关闭文件
try:
    f3_path = "base16.txt"
    with open(f3_path, "r+", encoding="utf-8") as f3:
        print(f3.readline())
        # 逐行读取文件
        for line in f3:
            print(line)
        # f.write(string) 把 string 的内容写入文件，并返回写入的字符数。
        f3.write("写入数据")
        # f.tell() 返回整数，给出文件对象在文件中的当前位置，表示为二进制模式下时从文件开始的字节数，以及文本模式下的意义不明的数字。
        print("f3.tell: ", f3.tell())
        # f.seek(offset, whence) 可以改变文件对象的位置。通过向参考点添加 offset 计算位置；参考点由 whence 参数指定。
        # 改变访问文件的游标


except FileNotFoundError:
    print("打开失败,没有找到指定的文件")

# 使用json读取结构化数据
# 需要导入json标准模块:import json
# json模块有两个重要的方法,分别是dump和load
# dumps(obj):将obj对象序列化为json对象返回
# dump(obj, fp):将结构化数据写入到指定文件中
#   obj就是要写入json文件的结构化数据
#   fp是指定的文件指针
# loads(str): 将字符串str转化为json数据
# load(fp):将指定文件中的数据加载为json对象
#   fp是指定的文件指针

import json

students = [
    {"name": "s1", "score": 78},
    {"name": "s2", "score": 65},
    {"name": "s3", "score": 99},
    {"name": "s4", "score": 90},
    {"name": "s5", "score": 51},
]

with open("base16.json", "w", encoding="utf-8") as f:
    json.dump(students, f)
    print("数据写入json成功")

with open("base16.json", "r+", encoding="utf-8") as f:
    json_data = json.load(f)
    print("读取json成功: ", type(json_data))
    print(json_data)
    for student in json_data:
        print(student["name"], student["score"])

# 文件指针（游标cursor）

# f = open("base16.txt", "w+", encoding="utf-8")
# print(f.readline())
# f.write("hello")
# f.flush()
# f.close()
# print("文件写入成功")

# 通过文化指针读取指定位置的数据, 使用 tell 和 seek
# teel(): 显示文件中当前位置，即文件指针当前所在位置
# seek(offset, whence)：移动文件指针到指定位置，
#   offset就是当前的偏移量字节数
#   whence是移动的起始位置，默认是0表示从头开始计算的位置，1表示从当前位置开始，2表示从为文件末尾开始

f = open("base16.txt", "w+", encoding="utf-8")
f.write("https://docs.python.org/zh-cn/3.10/tutorial/inputoutput.html")
f.flush()
print("当前位置：", f.tell())
f.seek(5, 0)
print(f.readline())
f.close()

# 以下实现二级制数据复制功能
with open("test.png", "rb") as f:
    # 创建新文件
    with open("test_copy.png", "wb") as f2:
        f2.write(f.read())
    print("文件复制成功")
