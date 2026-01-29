import numpy
import numpy as np


def test00():
    arr = np.array([[1, 2, 3], [4, 5, 6]])

    print(arr)
    print(arr.ndim)
    print(arr.shape)  # (2,3)，表示2行，3列
    print(arr.size)

    pass


def test01():
    # numpy的多维性
    arr0 = np.array(5)
    print(arr0)
    print(arr0.ndim)
    print(arr0.shape)
    print(arr0.size)
    print()

    arr1 = np.array([1, 2, 3])
    print(arr1)
    print(arr1.ndim)
    print(arr1.shape)
    print(arr1.size)
    print()

    arr2 = np.array([[1, 2, 3], [4, 5, 6]])
    print(arr2)
    print(arr2.ndim)
    print(arr2.shape)  # (2,3)，表示2行，3列
    print(arr2.size)
    print()

    arr3 = np.array([[1], [2], [3]])
    print(arr3)
    print(arr3.ndim)
    print(arr3.shape)
    print(arr3.size)
    print()

    # numpy的同质性，同一列的数据类型必须相同

    arr21 = numpy.array([123, 'abc'])
    print(arr21)  # ['123' 'abc'] 不同的数据类型会被转化为同一种类型
    print(type(arr21))
    print(arr21.ndim)
    print(arr21.shape)
    print(arr21.dtype)  # dtype -->>> data type
    print(arr21[0].dtype)  # dtype -->>> data type
    print(arr21[1].dtype)  # dtype -->>> data type
    print(arr21.T)
    print(arr21.T.shape)
    print(arr21.itemsize)  # 当个元素占用的字节数
    print(arr21.nbytes)  # 数组总共占用的字节数 = size * itemsize
    print(arr21.flags)  # 内存存储方式

    print(numpy.array([1, 1.23]))  # [1.   1.23]

    pass


if __name__ == "__main__":
    print(np.__version__)

    test01()

    pass
