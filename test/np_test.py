import numpy as np
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

na = np.arange(10)
print(na)

na = np.arange(10, 100, 2)
print(na)

na = np.arange(10).reshape(2, 5)
print(na)

na = np.eye(10)
print(na)