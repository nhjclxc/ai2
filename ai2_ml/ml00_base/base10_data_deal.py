import pandas as pd
import numpy as np
import sklearn
from sklearn import model_selection

"""
# 常用的数据打乱方法
| 方法                                                            | 适用对象      | 是否保持 X/y 对齐 | 是否支持随机种子 | 特点    |
| ------------------------------------------------------------- | --------- | ----------- | -------- | ----- |
| `np.random.shuffle()`                                         | NumPy数组   | ✅ 需自己写索引    | ✅        | 轻量，灵活 |
| `pandas.sample()`                                             | DataFrame | ✅           | ✅        | 语法简洁  |
| `sklearn.utils.shuffle()`                                     | X, y      | ✅ 自动        | ✅        | 推荐常用  |
| `train_test_split(..., shuffle=True)`                         | 切分数据集     | ✅           | ✅        | 一步完成  |
| `tf.data.Dataset.shuffle()` / `DataLoader(..., shuffle=True)` | 深度学习框架    | ✅           | ✅        | 大数据场景 |
"""

def test1(df: pd.DataFrame):
    # 方法1: np.random.shuffle()

    # X = df.drop('medv', axis=1).to_numpy()
    # y = df['medv'].to_numpy()
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y = np.array([0, 0, 1, 1])

    # 生成随机排列的索引
    indices = np.arange(X.shape[0])  # 将0到X.shape[0]的数字随机打乱，返回0到X.shape[0]随机的索引列表
    np.random.shuffle(indices)
    print('indices', indices, len(indices), '\n\n')

    # 根据索引重新排列
    X_shuffled = X[indices]
    y_shuffled = y[indices]

    print(X_shuffled, X_shuffled.shape)
    print(y_shuffled, y_shuffled.shape)


    pass


def test2(df: pd.DataFrame):
    # 方法2: pandas.sample()， 是 Pandas 用来随机抽样的函数。

    df = pd.DataFrame({
        "x1": [1, 2, 3, 4],
        "x2": [10, 20, 30, 40],
        "label": [0, 0, 1, 1]
    })
    print(df)
    print()

    # 打乱所有行
    # frac – Fraction of axis items to return. Cannot be used with n.
    # frac - 参数表示 抽取的样本占原 DataFrame 的比例，frac=1 表示抽取 100% 的数据，也就是说，返回一个和原 DataFrame 行数一样的随机排列。
    # random_state - 随机种子
    # .reset_index(drop=True)，可以重置索引，得到一个完全打乱顺序的新 DataFrame。
    df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
    print(df_shuffled)


def test3(df: pd.DataFrame):
    # 方法3: sklearn.utils.shuffle()

    # X = df.drop('medv', axis=1).to_numpy()
    # y = df['medv'].to_numpy()
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y = np.array([0, 0, 1, 1])
    print(X, X.shape)
    print(y, y.shape)
    print()

    X_shuffled, y_shuffled = sklearn.utils.shuffle(X, y, random_state=42)
    print(X_shuffled, X_shuffled.shape)
    print(y_shuffled, y_shuffled.shape)


    pass


def test4(df: pd.DataFrame):
    # train_test_split(..., shuffle=True)

    # X = df.drop('medv', axis=1).to_numpy()
    # y = df['medv'].to_numpy()
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y = np.array([0, 0, 1, 1])
    print(X, X.shape)
    print(y, y.shape)
    print()

    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X, y, test_size=0.2, shuffle=True, random_state=42
    )
    print(X_train, X_train.shape, X_test, X_test.shape)
    print(y_train, y_train.shape, y_test, y_test.shape)

    pass



if __name__ == "__main__":

    df = pd.read_csv('../../data/ml/BostonHousing.csv')

    # test1(df)
    # test2(df)
    # test3(df)
    # test4(df)
    # test5(df)

    print("常用的数据处理方法 - 数据打乱方法")
