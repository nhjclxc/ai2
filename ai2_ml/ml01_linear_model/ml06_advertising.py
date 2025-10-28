import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split

import loguru

"""
案例：广告投放效果预测
Advertising数据集：https://www.kaggle.com/datasets/tawfikelmetwally/advertising-dataset。
    	ID：序号
    	TV：电视广告投放金额，单位千元
    	Radio：广播广告投放金额，单位千元
    	Newspaper：报纸广告投放金额，单位千元
    	Sales：销售额，单位百万元
"""
if __name__ == '__main__':

    # 1、读取数据
    advertising = pd.read_csv('../../data/ml/advertising.csv')
    print(advertising.head(5), advertising.shape)

    # 2、数据缺失处理
    advertising.fillna(advertising.median(), inplace=True)

    # 原始数据的表头是："","TV","Radio","Newspaper","Sales"。第一列是id，因此要删除第一列的数据
    # 3、特征工程
    # advertising = advertising.drop("id", axis=1)
    # 在某个特征没有特征名称的时候，通过df.columns[0]的方式对齐进行操作
    advertising = advertising.drop(advertising.columns[0], axis=1)  # ✅ 删除第一列（axis=1 表示列）

    # 4、数据划分
    X = advertising.drop('Sales', axis=1)
    y = advertising['Sales']
    X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size=0.15, random_state=32)
    X_train, X_validation, y_train, y_validation = train_test_split(X_train_full, y_train_full, test_size=0.15, random_state=32)

    # 5、定义模型
    model = linear_model.LinearRegression()

    # 6、模型训练
    model.fit(X_train, y_train)

    print("模型训练完成：", model.coef_, model.intercept_)
    print("模型测试分数：", model.score(X_test, y_test))



    pass


