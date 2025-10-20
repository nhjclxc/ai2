#
import time

import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
"""
3.4 案例：心脏病预测
3.4.1 数据集说明
Heart Disease数据集 https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset
	年龄：连续值
	性别：0-女，1-男
	胸痛类型 cp：0-典型心绞痛，1-非典型心绞痛，2-非心绞痛，3-无症状
	静息血压：连续值，单位mmHg
	胆固醇：连续值，单位mg/dl
	空腹血糖：1-大于120mg/dl，0-小于等于120mg/dl
	静息心电图结果 restecg：0-正常，1-ST-T异常，2-可能左心室肥大
	最大心率：连续值
	运动性心绞痛：1-有，0-无
	运动后的ST下降：连续值
	峰值ST段的斜率 slope：0-向上，1-水平，2-向下
	主血管数量：0到3
	地中海贫血 thal：一种先天性贫血，0-正常，1-固定缺陷，2-可逆缺陷
	是否患有心脏病：标签，0-否，1-是

age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target

# KNN 核心思想：给定一个待预测样本，找到训练集中距离它最近的 K 个邻居，根据这些邻居的标签来进行预测。

"""

def feature_deal(heart_disease: pd.DataFrame, *, dropFirstColumn=False):
    """
    	类别型特征（需要特殊处理）
        	胸痛类型：4种分类（名义变量），cp：0-典型心绞痛，1-非典型心绞痛，2-非心绞痛，3-无症状，cp1,cp2,cp3,cp4每一个都对应0，1
        	静息心电图结果：3种分类（名义变量）, restecg：0-正常，1-ST-T异常，2-可能左心室肥大，restecg1,restecg2,restecg3
        	峰值ST段的斜率：3种分类（有序变量），slope：0-向上，1-水平，2-向下，slope1,slope2,slope3
        	地中海贫血：4种分类（名义变量），thal：一种先天性贫血，0-正常，1-固定缺陷，2-可逆缺陷，thal1,thal2,thal3

    对于类别型特征，直接使用整数编码的类别特征会被算法视为有序数值，
    导致错误的距离计算（例如：会认为 胸痛类型=1 和 胸痛类型=2 之间的差异比 胸痛类型=1和 胸痛类型=3之间差异更小，而实际上它们都是类别）。
    使用 独热编码（One-Hot Encoding）可将类别特征转换为二元向量，消除虚假的顺序关系。
    """
    print("开始处理多维特征。", heart_disease.shape)
    # 处理 cp
    cp1 = np.array([1 if cp == 0 else 0 for cp in heart_disease['cp']])
    cp2 = np.array([1 if cp == 1 else 0 for cp in heart_disease['cp']])
    cp3 = np.array([1 if cp == 2 else 0 for cp in heart_disease['cp']])
    cp4 = np.array([1 if cp == 3 else 0 for cp in heart_disease['cp']])
    # deal_cp = np.vstack([heart_disease['cp'], cp1, cp2, cp3, cp4]).T  # 垂直
    # print('deal_cp.shape', deal_cp.shape)
    # print(deal_cp[16:30])
    # 将独热编码后的cp放回去df里面，并且同时删除原有的cp
    if not dropFirstColumn:
        heart_disease['cp1'] = cp1
    heart_disease['cp2'] = cp2
    heart_disease['cp3'] = cp3
    heart_disease['cp4'] = cp4
    heart_disease = heart_disease.drop('cp', axis=1)
    # print(heart_disease.head(30))

    # 处理 restecg
    restecg1 = np.array([1 if cp == 0 else 0 for cp in heart_disease['restecg']])
    restecg2 = np.array([1 if cp == 1 else 0 for cp in heart_disease['restecg']])
    restecg3 = np.array([1 if cp == 2 else 0 for cp in heart_disease['restecg']])
    if not dropFirstColumn:
        heart_disease['restecg1'] = restecg1
    heart_disease['restecg2'] = restecg2
    heart_disease['restecg3'] = restecg3
    heart_disease = heart_disease.drop('restecg', axis=1)

    # 处理 slope
    slope1 = np.array([1 if cp == 0 else 0 for cp in heart_disease['slope']])
    slope2 = np.array([1 if cp == 1 else 0 for cp in heart_disease['slope']])
    slope3 = np.array([1 if cp == 2 else 0 for cp in heart_disease['slope']])
    if not dropFirstColumn:
        heart_disease['slope1'] = slope1
    heart_disease['slope2'] = slope2
    heart_disease['slope3'] = slope3
    heart_disease = heart_disease.drop('slope', axis=1)

    # 处理 thal
    thal1 = np.array([1 if cp == 0 else 0 for cp in heart_disease['thal']])
    thal2 = np.array([1 if cp == 1 else 0 for cp in heart_disease['thal']])
    thal3 = np.array([1 if cp == 2 else 0 for cp in heart_disease['thal']])
    if not dropFirstColumn:
        heart_disease['thal1'] = thal1
    heart_disease['thal2'] = thal2
    heart_disease['thal3'] = thal3
    heart_disease = heart_disease.drop('thal', axis=1)

    print("结束处理多维特征。。。", heart_disease.shape)

    return heart_disease
    pass



if __name__ == '__main__':

    # 1、读取数据
    heart_disease = pd.read_csv('../../data/heart-disease.csv')
    # print(heart_disease.describe(), heart_disease.shape)

    # 2、处理数据缺失值
    heart_disease.dropna()
    # heart_disease.info()
    # heart_disease.head()

    # 3、特征工程
    # drop="first"是独热编码中的一个参数，它的核心目的是避免多重共线性（Multicollinearity）。
    # 在独热编码时设置drop = "first"，会删除每个类别特征的第1列，从而打破完全共线性。
    feature_deal_heart_disease = feature_deal(heart_disease, dropFirstColumn=True)

    # 4、数据划分
    X = feature_deal_heart_disease.drop('target', axis=1)
    y = feature_deal_heart_disease['target']
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3, shuffle=True, random_state=42)
    # print(X_train, X_train.shape, X_test, X_test.shape)
    # print(y_train, y_train.shape, y_test, y_test.shape)

    # 5、定义KNN模型
    KNN = KNeighborsClassifier(n_neighbors=3)

    # 6、模型训练
    start_time = time.time()  # 记录开始时间
    KNN.fit(X_train, y_train)  # 模型训练
    end_time = time.time()  # 记录结束时间
    print(f"训练耗时: {end_time - start_time:.4f} 秒")

    # 7、模型评估，计算准确率
    knn_score = KNN.score(X_test, y_test)
    print('knn_score', knn_score)

    y_pred = KNN.predict(X_test)
    y_test_pred = np.vstack([y_test, y_pred, y_test == y_pred]).T
    print(y_test_pred, y_test_pred.shape, y_test_pred[:,2].sum()/y_test_pred.shape[0])

# 开始处理多维特征。 (1025, 14)
# 结束处理多维特征。。。 (1025, 19)
# 训练耗时: 0.0021 秒
# knn_score 0.8831168831168831
# (308, 3) 0.8831168831168831
    print('aaa')
