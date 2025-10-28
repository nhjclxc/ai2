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
    将 cp, restecg, slope, thal 转成独热编码

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
    heart_disease = pd.read_csv('../../data/ml/heart-disease.csv')
    # print(heart_disease.describe(), heart_disease.shape)

    # 2、处理数据缺失值
    heart_disease = heart_disease.dropna()
    # heart_disease.fillna(heart_disease.median(), inplace=True)
    # heart_disease.info()
    # heart_disease.head()

    # 3、特征工程
    # drop="first"是独热编码中的一个参数，它的核心目的是避免多重共线性（Multicollinearity）。
    # 在独热编码时设置drop = "first"，会删除每个类别特征的第1列，从而打破完全共线性。
    # feature_deal_heart_disease = feature_deal(heart_disease)
    # feature_deal_heart_disease = feature_deal(heart_disease, dropFirstColumn=True)
    # 手动独热编码冗长，容易出错, 可使用 pandas.get_dummies 一行解决，自动处理多列
    feature_deal_heart_disease = pd.get_dummies(
        heart_disease,
        columns=['cp', 'restecg', 'slope', 'thal'],
        drop_first=True  # 避免多重共线性
    )

    print("feature_deal_heart_disease: ", feature_deal_heart_disease.shape)
    # 4、数据划分
    X = feature_deal_heart_disease.drop('target', axis=1)
    y = feature_deal_heart_disease['target']
    # X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3, shuffle=True, random_state=42)
    # 划分训练集X_train、验证集X_val、测试集X_test
    X_train_full, X_test, y_train_full, y_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = model_selection.train_test_split(X_train_full, y_train_full, test_size=0.25, random_state=42)

    # print(X_train, X_train.shape, X_test, X_test.shape)
    # print(y_train, y_train.shape, y_test, y_test.shape)

    # 使用了原始数值（如 trestbps, chol, thalach 等），这些数值差异大，距离计算会偏向大数值特征, 而 KNN 又对特征尺度敏感。所以对其特征进行特征归一化/标准化处理
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 5、定义KNN模型
    KNN = KNeighborsClassifier(n_neighbors=2)

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
    print(y_test_pred.shape, y_test_pred[:, 2].sum() / y_test_pred.shape[0])

    """
    feature_deal_heart_disease:  (1025, 20)
    训练耗时: 0.0005 秒
    knn_score 0.9317073170731708
    (205, 3) 0.9317073170731708
    """

    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score

    best_k = 0
    best_acc = 0

    # 遍历不同的 K 值
    for k in range(1, 21):
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)  # 训练模型
        y_val_pred = knn.predict(X_val)  # 在验证集上预测
        acc = accuracy_score(y_val, y_val_pred)
        print(f"K={k}, 验证集准确率={acc:.4f}")

        if acc > best_acc:
            best_acc = acc
            best_k = k

    print("最优 K:", best_k, "验证集准确率:", best_acc)
    # 最优 K: 2 验证集准确率: 0.5756097560975609


    print('aaa')

"""
好的，我帮你系统地总结一下你提供的 **心脏病 KNN 代码**，以及 KNN 算法的核心知识点和注意事项。整理成两部分：代码总结 + KNN 知识总结。

---

## **一、心脏病 KNN 代码总结**

你的代码主要流程：

1. **读取数据**

   ```python
   heart_disease = pd.read_csv('../../data/heart-disease.csv')
   ```

   * 数据集共有 1025 条样本、14 个特征
   * 包含数值特征和类别特征（如 cp, restecg, slope, thal）

2. **处理缺失值**

   ```python
   heart_disease.dropna()
   ```

   * 这里应注意：`dropna()` 默认不修改原 DataFrame，需要赋值给变量或使用 `inplace=True`

3. **特征工程（类别型特征独热编码）**

   ```python
   feature_deal(heart_disease, dropFirstColumn=True)
   ```

   * 将 `cp, restecg, slope, thal` 转成独热编码
   * 避免 KNN 误认为类别特征是有序数值
   * `dropFirstColumn=True` 避免多重共线性

4. **划分训练集和测试集**

   ```python
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, random_state=42)
   ```

   * 测试集占 30%，训练集 70%
   * `shuffle=True` 确保样本顺序不会影响训练

5. **定义 KNN 模型**

   ```python
   KNN = KNeighborsClassifier(n_neighbors=3)
   ```

6. **训练模型**

   ```python
   KNN.fit(X_train, y_train)
   ```

7. **评估模型**

   ```python
   knn_score = KNN.score(X_test, y_test)
   print('knn_score', knn_score)
   ```

   * 得到准确率约 88%

8. **预测示例**

   ```python
   y_pred = KNN.predict(X_test)
   ```

   * 可以查看预测结果与真实值对比

---

### **代码优缺点**

**优点：**

* 流程完整：数据处理 → 特征工程 → 划分 → KNN → 评估
* 正确处理类别特征，避免虚假顺序
* 可复现（使用 `random_state`）

**待优化点：**

1. 手动独热编码冗长，可用 `pd.get_dummies`
2. 缺失值处理不修改原 DataFrame
3. 没有特征标准化，对 KNN 距离敏感
4. 没有验证集，KNN 超参数 `n_neighbors` 没有调优
5. 代码可以更模块化，函数化更清晰

---

## **二、KNN（K-Nearest Neighbors）算法总结**

### 1️⃣ 算法定义

* **KNN** 是一种**基于实例的监督学习算法**
* 可用于分类或回归
* 核心思想：**给定一个样本，找到训练集中距离最近的 K 个样本，根据它们的标签来决定预测结果**

---

### 2️⃣ 算法流程

**分类任务：**

1. 计算待预测样本与训练集每个样本的距离（欧氏距离或其他度量）
2. 选出距离最近的 K 个邻居
3. 统计 K 个邻居中标签出现次数，选择**出现次数最多的类别**作为预测

**回归任务：**

* 用 K 个邻居的平均值或加权平均作为预测值

---

### 3️⃣ 关键超参数

| 参数                | 作用      | 影响                  |
| ----------------- | ------- | ------------------- |
| K (`n_neighbors`) | 最近邻数量   | K 小 → 过拟合，K 大 → 欠拟合 |
| 距离度量              | 欧氏、曼哈顿等 | 不同度量会影响邻居选择         |
| 权重                | 距离加权或均等 | 距离加权可让近邻影响更大        |

---

### 4️⃣ 注意事项

1. **特征缩放**

   * KNN 对特征尺度敏感，需归一化或标准化
2. **类别特征处理**

   * 类别特征需独热编码，避免被算法误认为有序数值
3. **数据量问题**

   * KNN 训练简单，但预测需要计算所有训练样本距离
   * 大数据集时预测开销大，可使用 KD-Tree 或 Ball-Tree 优化
4. **噪声敏感**

   * KNN 对离群点敏感，K 值选择合理可缓解
5. **验证集调参**

   * 使用验证集或交叉验证选择最优 K

---

### 5️⃣ KNN 总结口诀

> **“靠近的朋友决定你是谁”**
>
> * 近邻的数量 K 决定平滑度
> * 距离决定影响权重
> * 数据越干净，KNN 越准确

---

✅ **结合你的代码来看**

* 你的实现已经体现了 KNN 的基本流程
* 优化点主要在 **自动独热编码 + 特征标准化 + 验证集调参**
* 优化后准确率和稳定性会更高，代码也更简洁易读

---

如果你愿意，我可以帮你写一个 **优化后的完整 Heart Disease KNN Python 示例**，包含：

* 自动独热编码
* 特征标准化
* 验证集调参 `n_neighbors`
* 最终训练与测试评估

这样你可以直接运行并对比效果。

你希望我写吗？



"""