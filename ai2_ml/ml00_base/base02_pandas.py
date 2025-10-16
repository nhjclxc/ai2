import pandas as pd


def test1(df):
    # 查看前5行
    print(df.head())
    # 查看后5行
    print(df.tail())
    # 查看纬度
    print(df.shape)
    # 查看列名
    print(df.columns)  # 可以认为是查看表头
    print(df.dtypes)
    # 快速统计信息
    print(df.describe())


def test2(df):
    # 3️⃣ 选择数据

    # ['name', 'age', 'score']

    # 选择列
    print(df['age'])
    print(df['name'])

    print('----------------')

    # 选择行
    print(df.loc[0])
    print()
    print(df.iloc[0])

    print()
    print(df.loc[1])
    print()
    print(df.iloc[1])
    print()

    # iloc按位置索引（integer-location），这个方法只能用索引，即数字访问，i是integer，索引
    # loc按标签索引（label-based），可以用索引或者列名
    # 选择行列
    print(df.iloc[0, 0], df.iloc[0, 1], df.iloc[0, 2])
    print(df.loc[0, 'name'], df.loc[0, 'age'], df.loc[0, 'score'])

    # 4️⃣ 条件筛选
    # 年龄大于 28
    print(df[df['age'] > 35])

    # 年龄大于 28 并且成绩大于 90
    print(df[(df['age'] > 30) & (df['score'] > 100)])

    print()
    print()
    # 5️⃣ 修改数据
    # 新增列
    df['passed'] = df['score'] > 90
    print(df)

    # 修改列
    df['score'] = df['score'] + 5
    print(df)
    # 如果原本有这一列了，即可以表示为更新该列
    df['passed'] = df['score'] > 90
    print(df)

    # 删除列
    df = df.drop('passed', axis=1)
    print(df)

    print()
    # 6️⃣ 缺失值处理
    print(df.isnull().sum())
    # 输出一下内容，name 0表示name这一列无缺失，表示age这一列缺失1个数据，表示score这一列缺失2个数据
    # name     0
    # age      1
    # score    2
    # dtype: int64

    # 删除含有缺失值的行
    # df_drop = df.dropna()  # 返回删除缺失行之后，无缺失数据的所有行，即该方法不改变原数据
    # print(df_drop)

    # 填充缺失值
    print(df)
    # df['age'].fillna(df['age'].mean(), inplace=True)  # 这种方法被弃用了，替换为下面两种新的方法
    df.fillna({'age': df['age'].mean()}, inplace=True)
    # df['age'] = df['age'].fillna(df['age'].mean())
    print(df.isnull().sum())
    print(df)
    """
FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.
The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a copy.

For example, when doing 'df[col].method(value, inplace=True)', try using 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead, to perform the operation inplace on the original object.

    """

    pass


def test3(df: pd.DataFrame):
    # 7️⃣ 排序与去重
    df_sorted = df.sort_values('age', ascending=False)
    print(df_sorted)
    df_sorted = df.sort_values(by=['age', 'score'], ascending=False)  # 先age，后score
    print(df_sorted)

    # 8️⃣ 分组统计（GroupBy）
    print(df.groupby('age'))
    print(df.groupby('age')['score'])
    print(df.groupby('age')['score'].mean())  # 按年龄统计分数的均值
    print(df.groupby('age')['score'].sum())  # 按年龄统计分数的和

    # 9️⃣ 数据合并与连接
    df1 = pd.DataFrame({'id': [1, 2, 3], 'score': [11, 22, 33]})
    df2 = pd.DataFrame({'id': [1, 2, 3], 'age': [18, 28, 38]})
    dfm = pd.merge(df1, df2, on='id')
    print(dfm)

    # axis=0按行拼接, axis=1按列拼接
    '''
| 参数    | axis=0 (默认) | axis=1    |
| ------ | -------------- | --------- |
| 作用    | 按行拼接        | 按列拼接      |
| 行/列变化 | 行数增加，列数不变   | 行数不变，列数增加 |
| 索引对齐  | 按列名对齐       | 按行索引对齐    |

    '''
    print(pd.concat([df1, df2], axis=0))
    print(pd.concat([df1, df2], axis=1))

    # 1️⃣0️⃣ 数学与统计操作
    print(df['score'].std())
    print(df['score'].mean())
    print(df['score'].max())
    print(df['score'].min())
    # print(df.corr())  # 相关系数
    # 应用函数
    print(df)
    df['score2'] = df['score'].apply(lambda x: x / 10)
    print(df)

    pass


def test5():
    """
1️⃣3️⃣ 实战小练习建议
    读取 BostonHousing.csv，计算每列和房价的相关系数。
    找出缺失值并填充平均值。
    按某一列分组统计平均房价。
    绘制房价与房间数的散点图。
    """
    df = pd.read_csv('./BostonHousing.csv')

    # 计算相关系数矩阵
    # 计算特征与房价 medv 的相关系数
    # 这个矩阵会计算每一列之间的相关系数，对角线上的元素都是1，并且是一个对称矩阵
    # 要知道其他条件与房价的相关系数是不是只要去除df.corr()的'medv'一列即可
    df_corr = df.corr()
    print('相关系数矩阵：', df_corr)
    df_corr_medv = df_corr['medv'].drop('medv')  # 去除其他特征与房价的相关系数，即只要df_corr['medv']这一列。此外，在去除房价对自己的相关系数就是其他所有特征对房价的相关系数
    print(df_corr_medv)
    print(df_corr['medv'])
    corr_with_target = df.corr()['medv'].sort_values(ascending=False)
    print("每列与房价的相关系数：\n", corr_with_target)

    # 找出缺失值并填充平均值
    print(df.isnull().sum())
    df_filled = df.fillna(df.mean())  # 用每列均值填充缺失值
    print(df_filled)

    # 按某一列age分组统计平均房价
    df_g_age_mean = df.groupby('age')['medv'].mean()
    print(df_g_age_mean)


    import seaborn as sns
    import matplotlib.pyplot as plt

    # 可视化热力图
    sns.heatmap(df_corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Feature Correlation Matrix")
    plt.savefig("plot.png")

    pass


if __name__ == '__main__':
    # 1. 从字典创建 DataFrame
    data = {
        "name": ["Alice", "Bob", "Charlie", "Bob22", "Charlie333"],
        "age": [25, 25, 35, 38, None],
        "score": [95.5, 92.0, None, 192.0, None]
    }
    df = pd.DataFrame(data)

    print(df)
    print()

    # test1(df)

    # test2(df)

    # test3(df)

    test5()

    print('\npd.__version__ = ', pd.__version__)
