import numpy as np


def test1():
    # 2️⃣ 数组创建

    arr = np.array([1, 2, 3, 4, 5, 6])
    print(arr, arr.shape, arr.dtype, end='\n\n')
    arr = arr.reshape((2, 3))
    print(arr, arr.shape, arr.dtype, end='\n\n')
    arr = arr.reshape((1, 6))
    print(arr, arr.shape, arr.dtype, end='\n\n')
    arr = arr.reshape((6, 1))
    print(arr, arr.shape, arr.dtype, end='\n\n')
    arr = arr.reshape((3, -1))
    print(arr, arr.shape, arr.dtype, end='\n\n')
    arr = arr.reshape((3, -1))
    print(arr, arr.shape, arr.dtype, end='\n\n')

    # 全0、全1、单位矩阵
    print(np.zeros(shape=(3, 4)))
    print(np.zeros((2, 6)))
    print(np.ones((4, 3)))
    print(np.ones((2, 3)))
    print(np.eye(3))
    print(np.eye(4))

    # 随机数组
    print(np.random.randn(3, 4))  # shape=(3,4)标准正态分布
    print(np.random.rand(3, 3))  # shape=(3,3)服从[0,1]的均匀分布
    print(np.random.randint(0, 10, size=(2, 5)))  # 整数
    print(np.random.uniform(1, 10, size=(2, 5)))  # 每个特征独立均匀分布在[1,10]
    print(np.random.uniform(1, 10, size=(2, 3)))  # 每个特征独立均匀分布在[1,10]

    pass


def test2():
    # 3️⃣ 数组基本操作
    x = np.array([1, 2, 3, 4, 5])
    print(x)

    # 形状调整
    x2 = x.reshape(1, 5)
    x3 = x.reshape(-1, 1)  # 自动推断行数
    print(x2)
    print(x3)

    # 展平
    print(x2, x2.shape, x2.dtype)
    flat = x2.ravel()  # 返回视图，修改返回值会 影响原数组（如果数据在内存中是连续的）
    flatten = x2.flatten()  # 返回 一个新的数组（复制），原数组不会改变。
    print(flat, flat.shape, flat.dtype)
    print(flatten, flatten.shape, flatten.dtype)

    # 数组连接
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    c = np.concatenate([a, b])
    c2 = np.vstack([a, b])  # 垂直
    c3 = np.hstack([a, b])  # 水平
    print(c, c.shape, c.dtype)
    print(c2, c2.shape, c2.dtype)
    print(c3, c3.shape, c3.dtype)


def test3():
    # 4️⃣ 索引与切片

    x = np.array([1, 2, 3, 4, 5, 6])
    print(x)
    print(x[2:5])  # 前必后开
    x.reshape(2, 3)
    print(x)
    x = x.reshape(2, 3)
    print(x)
    print(x[0,])
    print(x[1,:])
    print(x[:,2])

    x = np.array([1, 2, 3, 4, 5, 6])
    print([x[0,2]])  # [np.int64(3)]，那么如何输出 [3]

    pass


def test5():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])

    # 元素级运算
    print(a + b, a - b, a * b, a / b)
    print(a ** 2, np.sqrt(a), np.exp(a))

    # 点积 / 矩阵乘法
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    print(np.dot(A, B))
    print(A.dot(B), type(A))  # A是 <class 'numpy.ndarray'>类型的时候才能.dot()方法
    print(A @ B)

    # 广播机制
    x = np.array([[1], [2], [3]])
    y = np.array([10, 20])
    print(x + y)  # 自动广播，x的每一行都和y的每一列相加
    '''
    [[11 21]
     [12 22]
     [13 23]]
    '''

    pass


def test6():
    # 6️⃣ 统计函数

    arr = np.array([[1, 2, 3], [4, 5, 6]])

    # 基本统计
    print(np.sum(arr))
    print(np.mean(arr))
    print(np.std(arr))
    print(np.var(arr))
    print(np.min(arr), np.max(arr))
    print(np.argmin(arr), np.argmax(arr))
    print(np.median(arr))

    # 按轴统计
    print(np.sum(arr, axis=0))  # 列求和
    print(np.mean(arr, axis=1))  # 行求平均

    pass


def test7():
    # 7️⃣ 线性代数

    A = np.array([[1, 2], [3, 4]])
    b = np.array([5, 6])
    print(A)
    print(b)

    # 转置
    print(A.T)

    # 逆矩阵
    print(np.linalg.inv(A))

    # 行列式
    print(np.linalg.det(A))

    # 特征值和特征向量
    eigvals, eigvecs = np.linalg.eig(A)
    print(np.linalg.eig(A))

    # 解线性方程 Ax=b
    x = np.linalg.solve(A, b)
    print(np.linalg.solve(A, b))



if __name__ == '__main__':
    # numpy的基本使用

    # test1()

    test2()

    # test3()

    # test5()

    # test6()

    # test7()

    pass
