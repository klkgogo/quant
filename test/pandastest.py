import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame, Series

# 200只股票 504个交易日，服从正态分布涨跌幅数据
stock_cnt = 200
view_days = 504
stock_day_change = np.random.standard_normal((stock_cnt, view_days))
df = pd.DataFrame(stock_day_change)
print(df.head(5))
print("df[0,0]: ", df[0][0])
print("shape: ", df.shape)
print("df[0]", df[0])

stock_sym =['股票' + str(x) for x in range(df.shape[0])]
df = pd.DataFrame(stock_day_change, index = stock_sym)
print(df.head(5))

days = pd.date_range("2017-01-01", periods=stock_day_change.shape[1])

df = pd.DataFrame(stock_day_change, index = stock_sym, columns=days)
print(df.head(5))

df = df.T
print(df['股票0'])
stock0 = df['股票0']
plt.figure(0)
stock0.plot()
plt.figure(1)
stock0.cumsum().plot()
plt.show()
