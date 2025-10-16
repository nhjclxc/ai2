import functools

import numpy as np


def test1():
    """ ✅ 手动实现线性回归（梯度下降） """

    # 代码包括：数据生成 → 形状整理 → 参数初始化 → 训练循环（前向、求梯度、更新）→ 打印与单点预测验证。

    # ----------------------------------
    # 1.数据生成, 形状整理
    # ----------------------------------
    # 在[1,30]之间生成300个点，并且设置每个样本有3个特征，则有100个点，即有100个3个特征的样本
    # X = np.linspace(1, 30, 300).reshape(-1, 3)
    X = np.random.uniform(1, 30, size=(100, 3))
    # 根据 y=2x+3y+6z+8生成100个带有噪声的点
    # Y = 2 * X[:, 0] + 3 * X[:, 1] + 6 * X[:, 2] + 8 + np.random.randn(100, 1)  # 每个样本应该有独立噪声np.random.randn(100,1)
    Y = (2 * X[:, 0] + 3 * X[:, 1] + 6 * X[:, 2]).reshape(100, 1) + 8 + np.random.randn(100, 1)
    # (100, 3)100个样本每个样本3个特征， (100, 1)100个标签每个标签一个目标值
    print(X.shape, Y.shape)  # (100, 3) (100, 1)

    # 以下是模型训练的开始
    # ----------------------------------
    # 2.参数初始化
    # ----------------------------------
    w = np.random.randn(3).reshape(-1, 1)
    b = np.random.randn(1)[0]
    lr = 0.0001
    epochs = 10000
    print(w, w.shape, b, lr, epochs)  # w.shape=(3, 1)

    # ----------------------------------
    # 3.训练循环（前向、求梯度、更新）
    # ----------------------------------
    for epoch in range(epochs):
        # x.shape=(100,3), w.shape=(3,1), y_pred.shape=(100, 1)
        y_pred = X.dot(w) + b
        # print(X.shape, w.shape, y_pred.shape)
        # X.T.shape=(3,100),(Y - y_pred).shape=(100,1), (X.T.dot(Y - y_pred)).shape=(3,1), dw.shape=(3,1)也就是说3个特征分别有一个斜率
        dw = -2 * X.T.dot(Y - y_pred) / X.shape[0]  # X.shape[0]是特征个数，这里取0就是看一下第一个样本有多少个特征，即所有样本有多少个特征
        db = -2 * np.mean((Y - y_pred))
        w -= lr * dw
        b -= lr * db
        if epoch % 100 == 0:
            loss = np.mean((Y - y_pred) ** 2)
            print('epoch:', epoch, 'dw:', dw, 'db:', db, 'loss: ', loss)

    print(f"训练完成，w = {w}, b = {b}")

    # ----------------------------------
    # 预测
    # ----------------------------------
    def pred_fun0(w, b, x):
        # x.shape=(1,3), w.shape=(3,1),
        return x.dot(w) + b

    pred_fun = functools.partial(pred_fun0, w=w, b=b)
    xx = X[5]
    y_true = Y[5]
    pred_val = pred_fun(x=xx)

    print(f"x = {xx}, y_true = {y_true}, pred_val = {pred_val}, diff = {y_true - pred_val}")




if __name__ == "__main__":
    # 基于lm01_intro.py实现多特征的线形模型

    test1()

    print(np.mean([1, 2, 3, 4, 5]))
    print(np.mean([[1, 2], [3, 4], [5, 6]]))

    pass
