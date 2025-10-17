from collections import Counter

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

# 使用knn是实现房龄age的预测，除age外的其他列作为特征
# 用房价medv做特征，房龄age做标签

def euclidean_distance(x, y):
    """
        定义欧式距离
    :param x: x点所有点
    :param y: y点所有点
    """
    return np.sqrt(np.sum(x - y) ** 2)


if __name__ == "__main__":

    housing_data = pd.read_csv('./../../data/BostonHousing.csv')
    # (506, 14)
    print(housing_data.describe(), housing_data.shape)

    df_shuffled = housing_data.sample(frac=1, random_state=42).reset_index(drop=True)
    print(df_shuffled.describe(), df_shuffled.shape)

    X_train = df_shuffled['medv'][50:506]
    X_test = df_shuffled['medv'][50:506]
    y_train = df_shuffled['age'][:50]
    y_test = df_shuffled['age'][:50]
    print(X_train.shape, y_train.shape)
    print(X_test.shape, y_test.shape)

    K = int(np.sqrt(len(X_train)))

    for test_point in X_test:
        # 计算预测点与所有样本点的距离
        distances = [euclidean_distance(test_point, x_point) for x_point in X_train]
        # 取出tok-k个点
        topk = np.argsort(distances)[:K]
        # 计算topk出现的标签次数
        Counter(topk).most_common()

        pass


    pass


