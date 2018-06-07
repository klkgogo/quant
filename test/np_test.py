import numpy as np
import math
# one axis
a =[1,2,3]
na = np.array(a)
print(na)
print(na.ndim)
print(len(na))
print(na.shape)
print(na.dtype)

# two axis
a=[[1,2,3], [4,5,6]]
na = np.array(a)
print(na)
print(na.ndim)
print(len(na))
print(na.shape)
print(na.dtype)

# three axis
a=[[[1,2,3], [4,5,6]], [[7,8,9], [10,11,12]]]
na = np.array(a)
print(na)
print(na.ndim)
print(na.shape)
print(na.data)

# gen data
na = np.zeros(10)
print(na)

na = np.zeros((10,10))
print(na)

na = np.ones(10)
print(na)

# [0 1 2 3 4 5 6 7 8 9]
na = np.arange(10)
print(na)

# 0 ~ 10 间隔2
# [0 2 4 6 8]
na = np.arange(0, 10, 2)
print(na)

# 0~5, 10个数
'''
[0.         0.55555556 1.11111111 1.66666667 2.22222222 2.77777778
 3.33333333 3.88888889 4.44444444 5.        ]
'''
na = np.linspace(0, 5, 10)
print(na)

na = np.arange(10).reshape(2, 5)
print(na)

na = np.eye(10)

a = np.array([1,2,3,4])
b = np.array([6,7,8,9])
print(10 * a)
print(a + b)
print(a * b)
print(a.dot(b))
print(np.sin(a))
print(math.sin(a))  # 不能用python的sin



print(na)


a = np.arange(20)
print(a)
# [0 1 2 3 4]
print(a[0:5])
# [0 2 4]
print(a[0:5:2])
# [ 0  2  4  6  8 10 12 14 16 18]
print(a[0::2])
# [ 0  2  4  6  8 10 12 14 16 18]
print(a[::2])
# [5 4 3]
print(a[5:2:-1])
# revert
# [19 18 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0]
print(a[::-1])
#[ 2  1  2  3  2  5  2  7  2  9  2 11  2 13  2 15  2 17  2 19]
a[::2] = 2
print(a)
# [ 0  1  1  3  2  5  3  7  4  9  5 11  6 13  7 15  8 17  9 19]
a[::2] = np.arange(10)
print(a)
# [ True False  True False  True False  True False  True False  True False True False  True False  True False  True False]
a[::2] = 2
print(a == 2)

b = a[a == 2]
# [2 2 2 2 2 2 2 2 2 2]
print(b)
#[ 2  1  2  3  2  5  2  7  2  9  2 11  2 13  2 15  2 17  2 19]
print(a)

a[a == 2] = 3
#[ 3  1  3  3  3  5  3  7  3  9  3 11  3 13  3 15  3 17  3 19]
print(a)

b = a[a == 3]
b[::] = 4
#[ 3  1  3  3  3  5  3  7  3  9  3 11  3 13  3 15  3 17  3 19]
print(a)


"""
二维切片
"""
def f(x, y):
    return 10 * x + y
"""
[[ 0  1  2  3]
 [10 11 12 13]
 [20 21 22 23]
 [30 31 32 33]
 [40 41 42 43]]
"""
b = np.fromfunction(f, (5, 4), dtype=int)
print(b)

# 12
print(b[1,2])

# [11 21]
print(b[1:3, 1])

"""
[[10 11 12 13]
 [20 21 22 23]]
"""
print(b[1:3, :])

# [ 1 11 21 31 41]
print(b[:, 1])

# [10 11 12 13]
print(b[1])  #自动填充后面所有：和 b[1:]等价

# [10 11 12 13]
print(b[1, ...]) #...代表后面所有的：

# [ 1 11 21 31 41]
print(b[..., 1]) #...代表前面所有的：

"""
[[  0 100   2   3]
 [ 10 100  12  13]
 [ 20 100  22  23]
 [ 30 100  32  33]
 [ 40 100  42  43]]
"""
b[..., 1] = 100
print(b)

#Iterating
for row in b:
    print(row)
"""
[  0 100   2   3]
[ 10 100  12  13]
[ 20 100  22  23]
[ 30 100  32  33]
[ 40 100  42  43]
"""

for element in b.flat:
    print(element)
"""
0
100
2
3
10
100
12
13
20
100
22
23
30
100
32
33
40
100
42
43
"""

a = np.arange(20).reshape(5,4)
print(a)
"""
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]
 [12 13 14 15]
 [16 17 18 19]]
 """
b = a.reshape(4,5) # 不会改变自身
print(a)
"""
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]
 [12 13 14 15]
 [16 17 18 19]]
 """
print(b)
"""
[[ 0  1  2  3  4]
 [ 5  6  7  8  9]
 [10 11 12 13 14]
 [15 16 17 18 19]]
 """

b = a.resize(4,5)  #会改变a自身
print(a)
"""
[[ 0  1  2  3  4]
 [ 5  6  7  8  9]
 [10 11 12 13 14]
 [15 16 17 18 19]]
"""
print(b)
"""
None
"""

b = a.reshape(2, -1) # -1，自动计算这一维的值
print(b)