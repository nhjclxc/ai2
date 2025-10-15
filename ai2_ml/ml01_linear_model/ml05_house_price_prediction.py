

# 代码来源
# https://gitee.com/tony_cao/machine-learning/blob/master/regression/linear-regression/boston-house-prediction/house_price_prediction.py

import pandas as pd
import numpy as np

"""
| 列名        | 含义                                                                                          |
| --------- | ------------------------------------------------------------------------------------------- |
| `crim`    | 城镇人均犯罪率（per capita crime rate by town）                                                      |
| `zn`      | 占地面积超过 25,000 平方英尺的住宅用地比例（proportion of residential land zoned for lots over 25,000 sq.ft.） |
| `indus`   | 城镇非零售业务用地比例（proportion of non-retail business acres per town）                               |
| `chas`    | 查理斯河虚拟变量（Charles River dummy variable: 1 if tract bounds river; 0 otherwise）                |
| `nox`     | 一氧化氮浓度（nitrogen oxides concentration, parts per 10 million）                                 |
| `rm`      | 每户平均房间数（average number of rooms per dwelling）                                               |
| `age`     | 1940 年之前建成的自用房屋比例（proportion of owner-occupied units built prior to 1940）                   |
| `dis`     | 与波士顿五个中心区域的加权距离（weighted distances to five Boston employment centres）                       |
| `rad`     | 高速公路可达性指数（index of accessibility to radial highways）                                        |
| `tax`     | 每 10,000 美元的财产税率（full-value property-tax rate per $10,000）                                  |
| `ptratio` | 镇上师生比例（pupil-teacher ratio by town）                                                         |
| `b`       | 城镇中黑人比例（1000(Bk - 0.63)^2，其中 Bk 是黑人比例）                                                      |
| `lstat`   | 低收入人口比例（% lower status of the population）                                                   |
| `medv`    | 住房中位数（Median value of owner-occupied homes in $1000s）                                       |

"""
if __name__ == "__main__":

    # 1、读取数据
    # house_data = pd.read_csv("ai2_ml/ml01_linear_model/BostonHousing.csv")
    house_data = pd.read_csv("/Users/lxc20250729/lxc/py/ai2/ai2_ml/ml01_linear_model/BostonHousing.csv")

    print(house_data, len(house_data), house_data.shape)  # [506 rows x 14 columns] 506

    # 2、数据预处理（BostonHousing.csv原始数据，将特征和房价放一起了，所以我们要把特征和房价分离出来）
    # axis – Whether to drop labels from the index (0 or 'index') or columns (1 or 'columns').
    feature = house_data.drop("medv", axis=1)  # axis=0删除某一行，axis=1删除某一列
    target = house_data["medv"]

    # 3、分割数据，将原始数据分割为训练集X_train, 测试集X_test, y_train, y_test
    # 问题：feature 是 DataFrame，target 是 Series，不能直接用 [:, :] 的 NumPy 切片方式，会报错。
    # 正确的方式应该用 .iloc 或 .values 转 NumPy。
    # 转为 NumPy 数组
    X = feature.values
    y = target.values.reshape(-1, 1)  # 确保 y 是二维列向量

    # 切分数据
    X_train = X[:250, :]
    y_train = y[:250, :]
    X_test = X[250:, :]
    y_test = y[250:, :]

    print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)


    pass