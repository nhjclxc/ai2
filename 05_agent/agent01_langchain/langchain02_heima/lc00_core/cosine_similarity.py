#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/4/27 21:04
# Module    : cosine_similarity.py
# explain   :

import math

from langchain_community.utils.math import cosine_similarity


def dot(vec_a, vec_b) -> float:
    """
        计算两个向量的点积
    """
    if vec_a is None or vec_b is None:
        raise ValueError("数据不能为空")

    if len(vec_a) != len(vec_b):
        raise ValueError("两个向量长度必须相等")

    dot_sum = 0
    for x, y in zip(vec_a, vec_b):
        dot_sum += x * y

    return dot_sum


def norm(vec) -> float:
    """
        计算向量的模长
    """

    norm_sum = 0
    for val in vec:
        norm_sum += val * val
    return math.sqrt(norm_sum)

def get_cos(vec1, vec2) -> float:
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))

vec1 = [0.5, 0.5]
vec2 = [0.7, 0.7]
vec3 = [0.7, 0.5]

print(get_cos(vec1, vec2))
print(get_cos(vec1, vec3))
print(get_cos(vec2, vec3))

