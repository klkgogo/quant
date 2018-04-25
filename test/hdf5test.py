import h5py
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame, Series

# 200只股票 504个交易日，服从正态分布涨跌幅数据
stock_cnt = 200
view_days = 504
stock_day_change = np.random.standard_normal((stock_cnt, view_days))
df = pd.DataFrame(stock_day_change)
# print(df.head(5))
# print("df[0,0]: ", df[0][0])
# print("shape: ", df.shape)
# print("df[0]", df[0])

stock_sym =['股票' + str(x) for x in range(df.shape[0])]
df = pd.DataFrame(stock_day_change, index = stock_sym)
print(df.head(5))

days = pd.date_range("2017-01-01", periods=stock_day_change.shape[1])

df = pd.DataFrame(stock_day_change, index = stock_sym, columns=days)


f = h5py.File("stock.h5", 'w')
f['data'] = df
f.close()

f = h5py.File("stock.h5", 'r')
f.keys()
print(f.keys())
a = f['data']
print(a[:][0:5])
print(type(a))
f.close()

d = pd.HDFStore('data/df.h5', 'w')
d['data'] = df
d.close()

f = pd.HDFStore('data/df.h5', 'r')
print(f['data'][:])
f.close()


f = pd.HDFStore("data/BABA/BABA0.h5", 'r')
data = f['data'][:]
print(data)
f.close()

fa = pd.HDFStore("data/baba.h5", 'w')
fa.put('data', data, format="table")
fa.close()

fa = pd.HDFStore("data/baba.h5", 'a')
f = pd.HDFStore("data/BABA/BABA1.h5", 'r')
data = f['data'][:]
fa.put('data', data, format="table", append=True)
f.close()
fa.close()


fa = pd.HDFStore("data/baba/us.baba.h5", 'r')
data = fa['data'][:]
fa.close()
print (data)


