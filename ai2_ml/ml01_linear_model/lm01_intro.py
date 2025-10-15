import functools

import numpy as np
import matplotlib

matplotlib.use('Agg')  # 非交互式后端，用于远程服务器

import matplotlib.pyplot as plt
from sklearn import linear_model


def test1():
    """ ✅ 手动实现线性回归（梯度下降） """

    # 以下全部数据都要转化为(50,1)的矩阵，不能是(50,)的列表数据，即计算的时候一定要把唯独对齐，否则矩阵扩散的时候会进行误差叠加，
    # 代码包括：数据生成 → 形状整理 → 参数初始化 → 训练循环（前向、求梯度、更新）→ 打印与单点预测验证。

    # 生成一些模拟数据
    # X：输入样本，共 50 个点，范围在 [0,10]。
    # y：目标输出，符合直线关系 y=3x+7，并加了一点噪声。
    # .reshape(-1, 1)：确保是二维矩阵，方便矩阵乘法。
    X = np.linspace(0, 10, 50)  # shape = (50,)
    print(X.shape, 111)  # (50,)
    y = 3 * X + 7 + np.random.randn(50) * 1  # y = 3x + 7 + 噪声， 最后的*1表示噪声在(0,1)之间浮动
    print(y.shape, 333)  # (50,)
    X = X.reshape(-1, 1)  # 转为二维 shape = (50,1)
    y = y.reshape(-1, 1)  # 确保 y 也是 (50,1)
    print(X.shape, 222)  # (50, 1)
    print(y.shape, 333)  # (50,)
    # 至此生成了50个X的样本数据（x为(50,1)的矩阵），和一个y的具有噪声干扰的标签数据（x为(50,)的列表）

    # 下面才开始进行模拟机器学习
    # 初始机器学习参数化参数
    w = np.random.randn(1)
    print(w.shape, 555)  # (1,)
    b = 0
    # lr = 0.01  # 学习率
    lr = 0.01  # 学习率

    # 梯度下降
    for epoch in range(1000):
        y_pred = X.dot(w) + b  # y_pred.shape = (50,)，长度为50的列表
        y_pred = y_pred.reshape(-1, 1)  # 确保 y 也是 (50,1)
        dw = -2 * np.mean((y - y_pred) * X)  # 计算损失
        db = -2 * np.mean(y - y_pred)  # 计算损失 执行梯度下降
        w -= lr * dw  # 参数更新
        b -= lr * db  # 参数更新
        if epoch % 100 == 0:
            loss = np.mean((y - y_pred) ** 2)
            print(epoch, dw, db, w, b, loss)

    # 学到的模型: y = 3.04x + 6.60
    print(f"学到的模型: y = {w[0]:.2f}x + {b:.2f}")

    # 假设使用上面学习好的参数来进行预测
    print(w.shape, w, b)

    def pred_fun(w, b, xx):
        return xx.dot(w) + b

    xx = np.array(X[5])
    y_true = np.array(y[5])
    print(xx, xx.shape)
    xx = xx.reshape(-1, 1)
    print(xx, xx.shape)
    pred = pred_fun(w, b, xx)
    # pred = lambda w, b, xx: xx.dot(w) + b
    print(f"x = {xx}, y_true = {y_true}, pred = {pred}, diff = {y_true - pred}")

    """
(50,) 111
(50,) 333
(50, 1) 222
(50, 1) 333
(1,) 555
0 -182.5074563378071 -30.54790690949299 [3.12374039] 0.3054790690949299
100 0.2864132610496631 -1.9144716493448752 [3.58016402] 2.914050748875196
200 0.17281211409192807 -1.155127705609249 [3.35588153] 4.413221766106579
300 0.10426900859086131 -0.6969651479157102 [3.22055703] 5.317771059402704
400 0.06291240755690822 -0.4205252934808293 [3.13890679] 5.863545633882909
500 0.03795922756046146 -0.2537307969932053 [3.08964178] 6.192847628098868
600 0.022903319280615904 -0.1530926161656459 [3.05991694] 6.391537359107104
700 0.013819091372034364 -0.0923709277792944 [3.04198197] 6.511420050076278
800 0.008337974247694788 -0.05573350637352579 [3.03116061] 6.583753227644552
900 0.0050308528023730046 -0.03362772040256413 [3.02463137] 6.627396630498008
学到的模型: y = 3.02x + 6.65
(1,) [3.0207222] 6.65352669134538
[1.02040816] (1,)
[[1.02040816]] (1, 1)
x = [[1.02040816]], y_true = [10.15590993], pred = [9.73589628], diff = [0.42001365]

    """

    """"
关键注意点 / 已修正过的问题总结

形状一致性非常重要：X、y、y_pred 必须在运算时形状对齐，否则会触发 NumPy 广播产生错误梯度。你通过 reshape(-1,1) 修复了这个问题，这是核心修复步骤。

广播陷阱：若 y 为 (50,) 而 y_pred 为 (50,1)，表达式 (y - y_pred) 会触发广播，导致意外大矩阵，进而得到错误 dw。

权重形状更规范的写法：可以把 w 初始化为 (1,1)，即 w = np.random.randn(1,1)，这样 X.dot(w) 直接返回 (50,1)，无需额外 reshape。

学习率与 epoch：你用 lr=0.01、epoch=1000，这是合理的，若想更精确可增大 epoch 或减小 lr，看收敛曲线决定。

噪声影响：数据有随机噪声，训练到接近真实线性关系后，个别点偏差仍会存在，这属于预期。
    """
    pass


def test2():
    # 代码包括：数据生成 → 形状整理 → 参数初始化 → 训练循环（前向、求梯度、更新）→ 打印与单点预测验证。

    # ----------------------------------
    # 1.数据生成, 形状整理
    # ----------------------------------
    # 生成[0,10]之间100个点，并且将形状设置为(100, 1)，100行1列（100个样本1个特征）
    X = np.linspace(0, 10, 100).reshape(-1, 1)
    # 假设我们的特征方程是：y=6x+9，因此根基次方程生成100个标签数据,np.random.randn(100).reshape(-1, 1)是误差
    Y = 6 * X + 9 + np.random.randn(100).reshape(-1, 1)
    print(X.shape, Y.shape)  # (100, 1) (100, 1)

    # 以下是模型训练的开始
    # ----------------------------------
    # 2.参数初始化
    # ----------------------------------
    # 目标函数 y=wx+b，这里位置的是w斜率和偏置b
    w = np.random.randn(1).reshape(-1, 1)
    b = np.random.randn(1)[0]
    lr = 0.01
    print(w, w.shape, b, lr)

    # ----------------------------------
    # 3.训练循环（前向、求梯度、更新）
    # ----------------------------------
    # 用于记录每轮 loss
    loss_history = []

    for epoch in range(500):
        # 下面5行代码就是我们所说的建模
        y_pred = X.dot(w) + b  # 执行模型（这个就是我们建的模型）
        dw = -2 * np.mean((Y - y_pred) * X)  # 梯度下降 MSE损失函数对 w, b 的梯度gradient
        db = -2 * np.mean((Y - y_pred))  # 梯度下降
        w -= lr * dw  # 参数更新 参数更新用梯度下降公式：param -= lr * gradient
        b -= lr * db  # 参数更新

        if epoch % 5 == 0 and epoch != 0:
            loss = np.mean((Y - y_pred) ** 2)
            loss_history.append(loss)
            print(epoch, dw, db, w, b, loss)

            # 早停（Early Stopping）策略
            # 为了避免过拟合，判断是否提前退出训练
            if len(loss_history) > 2 and abs(loss_history[-1] - loss_history[-2]) < 1e-6:  # 10^(-6)
                print("Loss 收敛，可以停止训练")
                break

    print(f"训练完成，w = {w}, b = {b}")

    # ----------------------------------
    # 预测
    # ----------------------------------
    def pred_fun0(w, b, x):
        return w * x + b

    pred_fun = functools.partial(pred_fun0, w=w, b=b)  # 使用偏函数来固定两个已经确定的参数
    xx = X[5]
    y_true = Y[5]
    pred_val = pred_fun(x=xx)

    print(f"x = {xx}, y_true = {y_true}, pred_val = {pred_val}, diff = {y_true - pred_val}")

    # -----------------------------
    # 5. 绘制 loss 曲线
    # -----------------------------
    # 绘制 loss 曲线
    plt.figure()
    plt.plot(loss_history)
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Loss Curve")
    plt.savefig("loss_curve.png")  # 保存到文件
    plt.close()

    # 绘制拟合图
    plt.figure()
    plt.scatter(X, Y, label="Original Data")
    plt.plot(X, X.dot(w) + b, color='red', label="Fitted Line")
    plt.legend()
    plt.savefig("fit_line.png")
    plt.close()

    pass


def test3():
    """
    ✅ 用 scikit-learn 实现
from sklearn.linear_model import LinearRegression

X = X.reshape(-1, 1)
model = LinearRegression()
model.fit(X, y)

print("系数:", model.coef_[0])
print("截距:", model.intercept_)


scikit-learn（简称 sklearn）是 Python 中最常用的机器学习库之一：https://scikit-learn.org
    """

    # -----------------------------
    # 2️⃣ 数据准备
    # -----------------------------
    X = np.linspace(0, 10, 100).reshape(-1, 1)
    # 假设我们的特征方程是：y=6x+9，因此根基次方程生成100个标签数据,np.random.randn(100).reshape(-1, 1)是误差
    Y = 6 * X + 9 + np.random.randn(100).reshape(-1, 1)
    print(X.shape, Y.shape)  # (100, 1) (100, 1)
    X = X.reshape(-1, 1)

    # -----------------------------
    # 3️⃣ 创建模型对象
    # -----------------------------

    model = linear_model.LinearRegression()

    # -----------------------------
    # 4️⃣ 训练模型（拟合）
    # -----------------------------
    model.fit(X, Y)

    # -----------------------------
    # 5️⃣ 查看参数
    # -----------------------------
    print("系数:", model.coef_)
    print("截距:", model.intercept_)
    print("输入特征数：", model.n_features_in_)  # 1

    # ----------------------------------
    # 预测
    # ----------------------------------
    xx = X[5]
    y_true = Y[5]
    y_pred = model.predict(xx.reshape(-1,1))
    print(f"x = {xx}, y_true = {y_true}, pred_val = {y_pred}, diff = {y_true - y_pred}, score = {model.score(X, Y)}")



    pass


if __name__ == "__main__":
    # 线形回归简单案例

    # test1()

    # test2()

    # x = np.random.randn(3)  # 功能：生成 3个服从标准正态分布（均值 μ=0，标准差 σ=1）的随机数
    # print(x)
    # xx = np.linspace(20, 30, 10)  # 是 NumPy 用于生成等间距数列的函数, 生成固定数量、均匀间隔的数列
    # print(xx)

    test3()


    print("Hello")

    pass
