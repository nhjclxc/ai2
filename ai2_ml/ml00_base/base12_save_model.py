from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
import pickle
import numpy as np

if __name__ == "__main__":

    # 以下要演示的是如何保存训练好的模型本身以及模型参数

    # 随机生成数据
    X, y = make_classification(n_samples=100, n_features=4, n_classes=2)
    # 定义模型
    model = LogisticRegression()
    # 训练模型
    model.fit(X, y)
    # 输出模型参数，将模型本身保存和将模型参数保存两种方法都写出来
    print("系数:", model.coef_)
    print("截距:", model.intercept_)
    # ...

    # 5️⃣ 保存模型本身（可以直接用pickle加载继续使用）
    with open("../../bin/logistic_model.pkl", "wb") as f:
        pickle.dump(model, f)

    # 6️⃣ 加载模型
    with open("../../bin/logistic_model.pkl", "rb") as f:
        loaded_model = pickle.load(f)

    print("加载后的系数:", loaded_model.coef_)
    print("加载后的系数:", loaded_model.intercept_)

    # 7️⃣ 只保存模型参数（coef_ 和 intercept_）到 npy 文件
    np.save("../../bin/coef.npy", model.coef_)
    np.save("../../bin/intercept.npy", model.intercept_)

    # 8️⃣ 加载参数
    coef_loaded = np.load("../../bin/coef.npy")
    intercept_loaded = np.load("../../bin/intercept.npy")

    print("加载的系数:", coef_loaded)
    print("加载的截距:", intercept_loaded)

    """
    系数: [[1.92225032 1.69632353 1.20114333 0.69495973]]
    截距: [1.68697237]
    加载后的系数: [[1.92225032 1.69632353 1.20114333 0.69495973]]
    加载后的系数: [1.68697237]
    加载的系数: [[1.92225032 1.69632353 1.20114333 0.69495973]]
    加载的截距: [1.68697237]
    """

    pass