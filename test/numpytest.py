import numpy as np
print(np.version.full_version)
a=[1,2,3,4,5,6,7,8,9,0]
arr = np.array(a)
b = arr.reshape(2,5)
print (b[0,:][b[0,:] > 2])
print(b, type(b), b.size, b.shape)
loc = np.where(b==2)
print (loc[1][0])

#normal list
l = [ 1, 2, 3]
l = l * 2
print("normal list:", l)

#numpy array
l = np.arange(3)
l = l * 2
print("numpy array: ", l)
print(type(l))

# eye
eye = np.eye(3)
print(eye)

# 200只股票 504个交易日，服从正态分布涨跌幅数据
stock_cnt = 200
view_days = 504
stock_day_change = np.random.standard_normal((stock_cnt, view_days))
print(stock_day_change.shape)
print(stock_day_change[0:3, :5])
print(stock_day_change[:3, :5])
print(stock_day_change[2::-1, 0:5])

print(stock_day_change[-2, :5])

# copy
tmp = stock_day_change[:2, :5].copy()
tmp[0][0] = 0
print(stock_day_change[:2, :5])

tmp = stock_day_change[:2, :5]
tmp[0][0] = 0
print(stock_day_change[:2, :5])

# filter
tmp = stock_day_change[:2, :5].copy()
mask = tmp > 0.5
print(mask)
print(tmp[mask])

tmp[tmp > 0.5] = 1
print(tmp)

tmp = stock_day_change[:2, :5].copy()
tmp[(tmp > 0.5) | (tmp < -0.5) ] = 1
print(tmp)

# diff
print("orig:\n", stock_day_change[:2, :5])
d = np.diff(stock_day_change[:2, :5])
print("diff, axic = 1:\n", d)

d2 = np.diff(stock_day_change[:2, :5], axis = 0)
print("diff, axis = 0:\n", d2)

# where
tmp = stock_day_change[:2, :5].copy()
tmp2 = np.where(tmp > 0.5, 1, tmp)
print("where > 0.5:", tmp2)

# 0.5< tmp < 1
tmp2 = np.where(np.logical_and(tmp > 0.5, tmp < 1), 1, 0)
print(" 0.5< tmp < 1:\n", tmp2)