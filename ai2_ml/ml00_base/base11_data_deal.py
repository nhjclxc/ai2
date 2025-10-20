import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

"""
数据集划分（dataset splitting）。

🧩 一、划分目的与比例
典型比例为：
    训练集（train set）：约 60%～80%，用于模型学习。
    验证集（validation set）：约 10%～20%，用于调参和早停。
    测试集（test set）：约 10%～20%，用于最终评估模型的泛化性能。
例如：训练集 70%，验证集 15%，测试集 15%。


| 方法              | 是否打乱 | 适用任务  | 优点     | 缺点        |
| ---------------- | ------ | ------- | -------- | --------- |
| Random Split     | ✅    | 通用    | 快速简单   | 类别不平衡时效果差 |
| Stratified Split | ✅    | 分类    | 类比例稳定  | 仅限分类任务    |
| K-Fold           | ✅    | 回归/分类 | 稳定评估   | 计算开销大     |
| Leave-One-Out    | ❌    | 小数据集  | 充分利用数据 | 非常慢       |
| TimeSeriesSplit  | ❌    | 时间序列  | 保持时间顺序 | 不可随机      |
| 手动划分          | 可选   | 通用    | 自由灵活   | 容易出错      |


"""

def test1(df: pd.DataFrame):

    # 方法1: Random Split
    # X = df.drop('medv', axis=1).to_numpy()
    # y = df['medv'].to_numpy()
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y = np.array([0, 0, 1, 1])
    print(X, X.shape)
    print(y, y.shape)
    print()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=42)
    print(X_train, X_train.shape, X_test, X_test.shape)
    print(y_train, y_train.shape, y_test, y_test.shape)




    pass


if __name__ == "__main__":

    df = pd.read_csv('../../data/BostonHousing.csv')

    test1(df)

    print("常用的数据处理方法")
