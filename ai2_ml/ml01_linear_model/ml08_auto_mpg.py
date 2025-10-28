import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

"""
auto-mpg.csv

| 列名             | 类型     | 含义                                      |
| -------------- | ------ | --------------------------------------- |
| `mpg`          | float  | **目标变量**，每加仑英里数（Miles per Gallon），即汽车油耗 |
| `cylinders`    | int    | 汽缸数                                     |
| `displacement` | float  | 排量（cubic inches）                        |
| `horsepower`   | float  | 马力                                      |
| `weight`       | float  | 汽车重量（pounds）                            |
| `acceleration` | float  | 加速度（0-60 mph 所需时间）                      |
| `model year`   | int    | 汽车型号年份（两位数，如 70 = 1970）                 |
| `origin`       | int    | 汽车产地（1=美国，2=欧洲，3=日本）                    |
| `car name`     | string | 汽车名称（非数值特征，一般不用于模型训练）                   |

"""
import time


def feature_deal(mpg_data: pd.DataFrame, *, dropFirstColumn=False):
    #   `model year`汽车型号年份（两位数，如 70 = 1970），将其转化为距离当前的年份大小
    #   `origin`汽车产地（1=美国，2=欧洲，3=日本），转化为独热编码，origin1,origin2,origin3，此外为了避免线形，删除第一个特征origin1
    #   `car name`汽车名称（非数值特征，一般不用于模型训练），将其转化为多个标签，类似于汽车产地

    # year = time.localtime().tm_year - (model year + 1900)
    year = np.array([time.localtime().tm_year - (mpg_data['model year'] + 1900)]).T
    mpg_data = mpg_data.drop('model year', axis=1)
    mpg_data['year'] = year

    # mpg_data = pd.get_dummies(
    #     mpg_data,
    #     columns=['origin'],
    #     drop_first=dropFirstColumn  # 避免多重共线性
    # )

    # 处理 thal
    # origin1 = np.array([1 if cp == 1 else 0 for cp in mpg_data['origin']])
    # origin2 = np.array([1 if cp == 2 else 0 for cp in mpg_data['origin']])
    # origin3 = np.array([1 if cp == 3 else 0 for cp in mpg_data['origin']])
    # if not dropFirstColumn:
    #     mpg_data['origin1'] = origin1
    # mpg_data['origin2'] = origin2
    # mpg_data['origin3'] = origin3
    # mpg_data = mpg_data.drop('origin', axis=1)
    mpg_data = pd.get_dummies(mpg_data, columns=['origin'], drop_first=True)

    # car name特征的取值太多了，有305种，因此这里先直接删除这个特征，305要用张量(embedding)去编码了
    mpg_data = mpg_data.drop('car name', axis=1)
    # car_name_list = mpg_data['car name'].to_numpy()
    # car_name_dict = {}
    # for car_name in car_name_list:
    #     car_name_dict[car_name] = True
    #
    # print(len(car_name_dict))

    return mpg_data


def feature_deal_question_mark(mpg_data: pd.DataFrame):
    # 遍历每个元素，如果该行存在'?'，则删除该行

    # 将 '?' 替换为 np.nan
    mpg_data = mpg_data.replace('?', pd.NA)

    # 删除含有缺失值（NaN）的行
    mpg_data = mpg_data.dropna()

    return mpg_data


if __name__ == '__main__':
    # 读取数据
    mpg_data = pd.read_csv('../../data/ml/auto-mpg.csv')

    # 遍历每个元素，如果该行存在'?'，则删除该行
    # 数据缺失处理
    mpg_data = feature_deal_question_mark(mpg_data)

    # 特征处理
    mpg_data_feature_dealed = feature_deal(mpg_data, dropFirstColumn=True)
    print("特征处理后的数据", mpg_data_feature_dealed.shape, mpg_data_feature_dealed.columns,
          mpg_data_feature_dealed.head(5))


    # 数据划分
    X = mpg_data_feature_dealed.drop('mpg', axis=1)
    y = mpg_data_feature_dealed['mpg']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=32)

    # 归一化，标准化，
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 定义模型
    model = LinearRegression()

    # 模型训练
    model.fit(X_train, y_train)

    # 预测
    score = model.score(X_test, y_test)
    print("模型得分：", score)
    y_pred = model.predict(X_test)
    # xx = np.vstack((y_test, y_pred, y_pred - y_test)).T
    # print(xx.shape, xx)

    pass

"""
处理流程：
1、读取数据
2、缺失值处理
3、特征处理
4、数据集划分
5、特征标准化
6、模型训练
7、模型评估

请问该流程是否正确，不正确的地方请指出要怎么修改
"""