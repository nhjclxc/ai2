import functools

import numpy as np

from sklearn import linear_model

from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

def test1():
    # LinearRegression

    # 数据
    X = np.random.rand(100, 3)
    y = 2 * X[:, 0] + 3 * X[:, 1] + 5 * X[:, 2] + 7 + np.random.randn(100)

    # 模型训练
    model = linear_model.LinearRegression()
    model.fit(X, y)

    print("系数:", model.coef_)
    print("截距:", model.intercept_)

    # 预测
    x_test = np.array([[0.5, 0.2, 0.1]])
    print("预测值:", model.predict(x_test))
"""
| 模型                     | 用途                   | 典型参数                                                           | 训练示例                                                                                                                           | 预测方法                                                       |
| ---------------------- | -------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- |
| **LinearRegression**   | 普通最小二乘线性回归（回归任务）     | `fit_intercept=True`、`normalize=False`                         | `python from sklearn.linear_model import LinearRegression model = LinearRegression() model.fit(X, y)`                          | `model.predict(X_test)`                                    |
| **Ridge**              | L2正则化线性回归，防止过拟合      | `alpha=1.0`、`fit_intercept=True`                               | `python from sklearn.linear_model import Ridge model = Ridge(alpha=1.0) model.fit(X, y)`                                       | `model.predict(X_test)`                                    |
| **Lasso**              | L1正则化线性回归，特征选择       | `alpha=0.1`、`max_iter=1000`                                    | `python from sklearn.linear_model import Lasso model = Lasso(alpha=0.1) model.fit(X, y)`                                       | `model.predict(X_test)`                                    |
| **ElasticNet**         | L1 + L2混合正则化         | `alpha=0.1`、`l1_ratio=0.7`                                     | `python from sklearn.linear_model import ElasticNet model = ElasticNet(alpha=0.1, l1_ratio=0.7) model.fit(X, y)`               | `model.predict(X_test)`                                    |
| **RidgeCV**            | 自动选择最优L2正则化参数        | `alphas=[0.1,1.0,10.0]`、`cv=5`                                 | `python from sklearn.linear_model import RidgeCV model = RidgeCV(alphas=[0.1,1,10], cv=5) model.fit(X, y)`                     | `model.predict(X_test)`                                    |
| **LassoCV**            | 自动选择最优L1正则化参数        | `cv=5`、`max_iter=1000`                                         | `python from sklearn.linear_model import LassoCV model = LassoCV(cv=5) model.fit(X, y)`                                        | `model.predict(X_test)`                                    |
| **LogisticRegression** | 分类任务（线性模型 + sigmoid） | `penalty='l2'`、`C=1.0`、`solver='lbfgs'`                        | `python from sklearn.linear_model import LogisticRegression model = LogisticRegression() model.fit(X, y_class)`                | `model.predict(X_test)` <br> `model.predict_proba(X_test)` |
| **SGDRegressor**       | 大规模数据线性回归（梯度下降优化）    | `loss='squared_loss'`、`learning_rate='invscaling'`、`eta0=0.01` | `python from sklearn.linear_model import SGDRegressor model = SGDRegressor(max_iter=1000, eta0=0.01) model.fit(X, y)`          | `model.predict(X_test)`                                    |
| **SGDClassifier**      | 大规模数据分类任务            | `loss='log'`、`max_iter=1000`                                   | `python from sklearn.linear_model import SGDClassifier model = SGDClassifier(max_iter=1000, loss='log') model.fit(X, y_class)` | `model.predict(X_test)` <br> `model.predict_proba(X_test)` |

"""


def test2():
    # LogisticRegression, 分类任务

    # ValueError: Number of informative, redundant and repeated features must sum to less than the number of total features
    X, y = make_classification(n_samples=100, n_features=4, n_classes=2)
    model = LogisticRegression()
    model.fit(X, y)
    print("系数:", model.coef_)
    print("截距:", model.intercept_)

    # 预测概率
    print(y[:5]) # [0 1 0 1 1]
    pro = model.predict_proba(X[:5])
    print(pro)
    '''
    输出如下，则表示X的前5个样本在n_classes=2的概率分别是多少，第一列是分类1的概率，第二列是分类2的概率
[[3.63540132e-02 9.63645987e-01]
 [1.32733537e-01 8.67266463e-01]
 [2.79821836e-01 7.20178164e-01]
 [2.30775556e-01 7.69224444e-01]
 [9.99859864e-01 1.40135551e-04]]
    '''
    print([0 if p[0] > p[1] else 1 for p in pro])  # [0, 1, 0, 1, 1]

    print(model.predict(X[:5]))  # [0, 1, 0, 1, 1]

    pass


if __name__ == "__main__":
    # 用 scikit-learn 实现各种线形模型
    # from sklearn import linear_model
    # LinearRegression：多项式,用途：单变量或多变量线性拟合，最基本的线性回归。

    # test1()

    test2()

    pass
