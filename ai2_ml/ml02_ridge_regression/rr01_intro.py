
# 最简单的岭回归示例
from sklearn.linear_model import Ridge
from sklearn.datasets import make_regression

if __name__ == "__main__":

    # 生成一个简单的回归数据集
    X, y = make_regression(n_samples=100, n_features=2, noise=10, random_state=42)

    # 创建岭回归模型，alpha对应正则化强度
    model = Ridge(alpha=1.0)

    # 训练模型
    model.fit(X, y)

    # 输出回归系数和截距
    print("回归系数:", model.coef_)
    print("截距:", model.intercept_)

    # 预测
    y_pred = model.predict(X)
    print("前5个预测值:", y_pred[:5])

    # from sklearn.linear_model import Ridge
    # from sklearn.model_selection import train_test_split
    # from sklearn.datasets import load_boston
    #
    # # 数据
    # X, y = load_boston(return_X_y=True)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    #
    # # 岭回归
    # ridge = Ridge(alpha=1.0)  # alpha 对应 λ
    # ridge.fit(X_train, y_train)
    #
    # print("回归系数：", ridge.coef_)
    # print("训练集R^2:", ridge.score(X_train, y_train))
    # print("测试集R^2:", ridge.score(X_test, y_test))


