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
# print(math.sin(a))  # 不能用python的sin



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

b = a.resize(4, 5)  #会改变a自身
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
"""
[[ 0  1  2  3  4  5  6  7  8  9]
 [10 11 12 13 14 15 16 17 18 19]]
 """

# Stacking together different arrays

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print(a)
"""
[[1 2]
 [3 4]]
 """
print(b)
"""
[[5 6]
 [7 8]]
 """

c = np.hstack((a, b))
print(c)
"""
[[1 2 5 6]
 [3 4 7 8]]
 """

c = np.vstack((a, b))
print(c)
"""
[[1 2]
 [3 4]
 [5 6]
 [7 8]]
 """

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
# The function column_stack stacks 1D arrays as columns into a 2D array. It is equivalent to hstack only for 2D arrays:
# 将一维数组作为二维数组的列
c = np.column_stack((a, b))
print(c)
"""
[[1 2 5 6]
 [3 4 7 8]]
"""
a = [1, 2]
b = [3, 4]
c = np.column_stack((a, b))
print(c)
"""
[[1 3]
 [2 4]]
 """

# concatenate Join a sequence of arrays along an existing axis.

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])
c = np.concatenate((a, b), axis= 0)
print(c)
"""
[[1 2]
 [3 4]
 [5 6]]
 """

c = np.vstack((a, b)) # same as above
print(c)
"""
[[1 2]
 [3 4]
 [5 6]]
"""
c = np.concatenate((a, b.T), axis=1)
print(c)
"""
[[1 2 5]
 [3 4 6]]
 """

#分割

a = np.array([[ 9.,  5.,  6.,  3.,  6.,  8.,  0.,  7.,  9.,  7.,  2.,  7.],
              [ 1.,  4.,  9.,  2.,  2.,  1.,  0.,  6.,  2.,  2.,  4.,  0.]])  # 2x12
c = np.hsplit(a, 3) #以3列为一组分开
print(c)
"""
[array([[9., 5., 6., 3.],
       [1., 4., 9., 2.]]), array([[6., 8., 0., 7.],
       [2., 1., 0., 6.]]), array([[9., 7., 2., 7.],
       [2., 2., 4., 0.]])]
       """
c = np.hsplit(a, (3, 5, 7)) #以第3，5，7列为分割点分开
print(c)
"""
[array([[9., 5., 6.],
       [1., 4., 9.]]), array([[3., 6.],
       [2., 2.]]), array([[8., 0.],
       [1., 0.]]), array([[7., 9., 7., 2., 7.],
       [6., 2., 2., 4., 0.]])]
"""

# copy 和 view
a = np.array([1, 2, 3])
b = a  # 赋值操作，a, b指向同一对像，这和python的赋值是一样的
b[0] = 4
print(id(a))
print(id(b))  # a,b 的id 相同
"""
55644032
55644032
"""

print(a) # 改变b,即改变a
"""
[4 2 3]
"""

def f(x):           # 参数传递也是引用传递
    print(id(x))
f(a)
"""
55644032
"""

# view
a = np.arange(10)
c = a.view()  # c是a的一个View
print(c is a) # c和a不是同一个object
print(id(c))
print(id(a))
"""
False
55643952
55642672
"""

print(c.base is a)  # 但c的底层数据是a的数据，c是a的数据的一个view
print(id(c.base))
print(id(a))
print(type(c))
"""
True
55970432
55970432
"""
c.shape = (2, 5)  #可以改变view的shape
print(c)
"""
[[0 1 2 3 4]
 [5 6 7 8 9]]
"""
print(a)     #但原来的a的shape不受影响
"""
[0 1 2 3 4 5 6 7 8 9]
"""

c[0,0] = 100   #改变数据会同时反映在c和a上，因为c和a共享同一分底层数据，只是view（视觉）不同
print(c)
"""
[[100   1   2   3   4]
 [  5   6   7   8   9]]
"""
print(a)
"""
[100   1   2   3   4   5   6   7   8   9]
"""

d = a[1:4]  #切片返回的是一个view
d[:] = 10
print(c)
"""
[[100  10  10  10   4]
 [  5   6   7   8   9]]
 """

#deep copy
d = a.copy()  # d和a是两个object底层数据也不相同
print(d.base is a)
"""
False
"""


"""
numpy特有的索引方法
"""

"""
使用list作为索引
"""
a = np.arange(10)
print(a[[1, 2, 3]])
"""
[1 2 3]
"""
i = np.array([[1, 2], [3, 4]])
print(a[i])
"""
[1 2]
 [3 4]]
 """

# 如果a是多维的，索引是沿着axis = 0
palette = np.array( [ [0,0,0],                # black
                     [255,0,0],              # red
                     [0,255,0],              # green
                     [0,0,255],              # blue
                     [255,255,255] ] )       # white
image = np.array([[0, 2, 1, 3],
                 [2, 3, 0, 0]])
print(palette[image])
"""
[[[  0   0   0]
  [  0 255   0]
  [255   0   0]
  [  0   0 255]]

 [[  0 255   0]
  [  0   0 255]
  [  0   0   0]
  [  0   0   0]]]
  """

#多维索引
a = np.arange(12).reshape(3,4)
print(a)
"""
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
"""
i = np.array([ [0, 1],
               [1, 2] ])
j = np.array([ [2, 3],
               [0, 2]])
print(a[i])
"""
[[[ 0  1  2  3]
  [ 4  5  6  7]]

 [[ 4  5  6  7]
  [ 8  9 10 11]]]
"""

print(a[i, j])
"""
[[ 2  7]
 [ 4 10]]
"""

# 使用索引赋值
a[i, j] = 0
print(a)
"""
[[ 0  1  0  3]
 [ 0  5  6  0]
 [ 8  9  0 11]]
 """

"""
boolean 索引
"""
a = np.arange(12).reshape(3,4)
b = a > 4
print(b)
"""
[[False False False False]
 [False  True  True  True]
 [ True  True  True  True]]
 """
print(a[b])
"""
[ 5  6  7  8  9 10 11]
"""
a[b] = 10  #赋值
print(a)
"""
[[ 0  1  2  3]
 [ 4 10 10 10]
 [10 10 10 10]]
"""

a = np.arange(12).reshape(3, 4)
print(a)
"""
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
 """
i = np.array([0, 1])
j = np.array([2, 3])
print(a[i, j])
"""
[2 7]
"""
b = a[i]
print(b)
"""
[[0 1 2 3 4]
 [5 6 7 8 9]]
 """
print(a[i, j])

"""
ix_
"""

ixgrid = np.ix_([0, 1], [2, 3])
print(ixgrid)
print(a[ixgrid])
"""
[[2 3]
 [6 7]]
"""
# ixgrid 相当于以下i,j
i = np.array([[0, 0],
             [1, 1]])
j = np.array([[2, 3],
             [2, 3]])
print(a[i, j])
"""
[[2 3]
 [6 7]]
 """

a = np.array([1, 2, 3])
b = np.array([5, 6, 7])
ax, bx = np.ix_(a, b)
print(ax)
"""
[[1]
 [2]
 [3]]
 """
print(bx)
"""
[[5 6 7]]
"""
result = bx + ax

print(result)
"""
[[ 6  7  8]
 [ 7  8  9]
 [ 8  9 10]]
 """
print(result[1,2])
"""
9
"""