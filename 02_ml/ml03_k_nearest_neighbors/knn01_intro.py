import numpy as np
from collections import Counter
from sklearn.neighbors import KNeighborsClassifier

# knn入门介绍
# K近邻算法（K-Nearest Neighbors，KNN）是一种基本的分类与回归方法，属于监督学习算法。
# 其核心思想是通过计算给定样本与数据集中所有样本的距离，找到距离最近的K个样本，然后根据这K个样本的类别或值来预测当前样本的类别或值。
# 核心思想：给定一个待预测样本，找到训练集中距离它最近的 K 个邻居，根据这些邻居的标签来进行预测。

def test1():
    """
    2️⃣ KNN工作原理
        训练阶段：
            KNN 实际上不需要显式训练（称为懒惰学习，lazy learning）
            保存训练集特征和标签即可
        预测阶段：
            计算待预测样本与训练集中所有样本的距离
            选择 最近的 K 个样本（邻居）
            根据邻居的标签进行预测：
                分类：多数表决（majority vote）
                回归：取邻居标签的平均值或加权平均

欧氏距离 (Euclidean)    | ( \sqrt{\sum_i (x_i - y_i)^2} ) | 最常用，适合连续数值

    """
    # 训练数据
    X_train = np.array([[1, 2], [2, 3], [3, 3], [6, 5], [7, 7], [8, 6]])
    y_train = np.array([0, 0, 0, 1, 1, 1])

    # 待预测样本
    X_test = np.array([[3, 2], [7, 5]])

    # K 值
    K = int(np.sqrt(len(X_train)))  # K = 3

    # 实现方法1:使用手动实现

    y_pred = []
    # 训练
    for x_point in X_test:
        # 计算待预测样本与训练集中所有样本的距离
        distances = [euclidean_distance(x_point, x) for x in X_train]
        # 选择 最近的 K 个样本（邻居）
        # distances.sort(reverse=True)
        # k_indices = distances[:K]
        # 2. 获取最近 K 个点的索引
        k_indices = np.argsort(distances)[:K]

        # 3. 找到这 K 个点对应的标签
        k_labels = y_train[k_indices]
        y_pred.append(my_counter(k_labels))
    y_pred2 = np.array(y_pred)
    print('y_pred2', y_pred2)


    # print("结果", np.concat(X_test, y_pred2))


    # 实现方法2:使用sklearn里面写好的方法实现

    y_pred = []
    for x_point in X_test:
        # 1. 计算 test_point 与训练集中每个点的距离
        distances = [euclidean_distance(x_point, x) for x in X_train]
        print('distances', distances)

        # 2. 获取最近 K 个点的索引
        k_indices = np.argsort(distances)[:K]
        print('k_indices', k_indices)

        # 3. 找到这 K 个点对应的标签
        k_labels = y_train[k_indices]
        # print('k_labels', k_labels)

        # 4. 多数投票
        # Counter(k_labels) 返回列表出现频次统计，.most_common(1)返回出现频次top-k，
        # 前面返回[('a', 5), ('b', 3),('c', 2)]，那么[0][0]表示获取出现频次最高的一个的标签即'a'
        most_common = Counter(k_labels).most_common(1)[0][0]
        y_pred.append(most_common)
        # print('most_common', most_common)

    print('y_pred1', y_pred)

    pass


def my_counter(k_labels: np.array):
    counter_dict = {}
    if len(k_labels):
        for k_label in k_labels:
            # key = k_label.item()
            # if key in counter_dict:
            #     counter_dict[key] += 1
            # else:
            #     counter_dict[key] = 1

            key = k_label.item()
            counter_dict[key] = counter_dict.get(key, 0) + 1
            # print('key', key, counter_dict.get(key))

    maxKey = None
    maxValue = None
    for key, value in counter_dict.items():
        if maxKey == None:
            maxKey = key
            maxValue = value
            continue
        if value > maxValue:
            maxKey = key
    # print(maxValue, maxKey)
    return maxKey


def euclidean_distance(x, y):
    """
        定义欧式距离
    :param x: x点所有点
    :param y: y点所有点
    """
    return np.sqrt(np.sum(x - y) ** 2)


def test2():
    # 简单训练集（特征：x1,x2；标签：0/1）

    X_train = np.array([[1, 2], [2, 3], [3, 3], [6, 5], [7, 7], [8, 6]])
    y_train = np.array([0, 0, 0, 1, 1, 1])

    # 待预测样本
    X_test = np.array([[3, 2], [7, 5]])

    # 1. 创建 KNN 分类器，K=3
    knn = KNeighborsClassifier(n_neighbors=3)

    # 2. 训练（KNN其实是懒惰学习，但sklearn需要fit）
    knn.fit(X_train, y_train)

    # 3. 预测
    y_pred = knn.predict(X_test)

    print("预测结果111:", y_pred)

    pass


if __name__ == "__main__":

    # test1()

    test2()

    pass
