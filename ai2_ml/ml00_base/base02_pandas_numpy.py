import numpy as np
import pandas as pd

"""
| 方向                    | 方法                                   | 输出类型      | 说明   |
| --------------------- | ------------------------------------ | --------- | ---- |
| pandas → numpy        | `df.to_numpy()`                      | `ndarray` | ✅ 推荐 |
| pandas → numpy        | `df.values`                          | `ndarray` | 旧写法  |
| pandas.Series → numpy | `s.to_numpy()`                       | `ndarray` | 单列   |
| numpy → pandas        | `pd.DataFrame(ndarray, columns=...)` | DataFrame | 可加列名 |
| numpy → pandas        | `pd.Series(ndarray, name=...)`       | Series    | 一维数据 |

"""

if __name__ == '__main__':
    # numpy和pandas数据互转
    # NumPy 提供底层的 ndarray 数组结构
    # pandas 的 DataFrame、Series 是在 ndarray 之上封装的更高级的数据结构

    names = ["Alice", "Bob", "Charlie", "Bob22", "Charlie333", "Jack"]
    ages = [25, 25, 35, 38, None, 66]
    scores = [95.5, 92.0, None, 192.0, None, 99]
    np_names = np.array(names)
    np_ages = np.array(ages)
    np_scores = np.array(scores)
    print(np_names)
    print(np_ages)
    print(np_scores, np_scores.shape)

    print("\n\n==========numpy → pandas===========\n")
    df_arr = pd.DataFrame(
        np.array([np_names, np_ages, np_scores]).T,
        # np.array([np_names, np_ages, np_scores])是(3,6)的 .T之后变成(6,3)即6个样本3个特征
        columns=['name', 'age', 'score']
    )
    print(df_arr, df_arr.describe())
    print(df_arr.index, df_arr.columns)

    print("\n\n==========pandas -> numpy===========\n")
    df = pd.DataFrame({
        "name": names,
        "age": ages,
        "score": scores
    })
    print(df)
    print(df.describe())

    arr = df.to_numpy()  # numpy.ndarray
    print(arr, arr.shape)

    # 将pd的单行提取为列表
    print(arr[0])
    print(arr[1])
    # 将pd的单列提取为列表
    print(df['name'])
    print(df['name'].to_numpy())
    print(df['age'])

    print("-----------混合示例（常用于机器学习）-----------\n")
    # 读取的原始数据和输出是 pandas，训练要的是 numpy，注意df里面的name一列不能直接输入训练，训练只能用数字，这里知识做一个演示效果
    # pandas → numpy划分 → 模型训练 → 模拟预测 → pandas回写

    # 1、读取原始数据
    print(df, df.shape)

    # 2、pandas数据转化为numpy，训练集:测试集:验证集 = 8:1:1  # 假设score是目标标签
    # 先将原始数据进行打乱
    # df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
    # df_shuffled = df.iloc[np.random.permutation(len(df))].reset_index(drop=True)
    n = df.shape[0]
    train_end = int(n * 0.8)  # [0, 8)的分给训练
    test_end = int(n * 0.9)  # 8分给测试，9 分给验证
    X_train = df[:train_end].drop('score', axis=1).to_numpy()
    y_train = df[:train_end]['score'].to_numpy()
    X_test = df[train_end:test_end].drop('score', axis=1).to_numpy()
    y_test = df[train_end:test_end]['score'].to_numpy()
    X_verify = df[test_end:].drop('score', axis=1).to_numpy()
    y_verify = df[test_end:]['score'].to_numpy()

    print(X_train, X_train.shape)
    print(X_test, X_test.shape)
    print(X_verify, y_verify.shape)

    # 3、numpy数据模型训练
    # model.fit(X_train, y_train)

    # 4、模型预测
    # pred = model.predict(X_test)  # 真实是这样的
    pred = np.array(['A', 'B', 'C', 'A', 'D', 'A+'])  # 这个是模拟，模拟输出是他们的等级标签

    # 5、numpy转化为pandas，即将预测数据转化为pandas存入文件或数据库
    # df['pred'] = pd.DataFrame(pred, columns=['pred'])
    df['pred'] = pred
    print(df, df.shape)

    # 6、将模型预测的数据输出或入库...

    pass
