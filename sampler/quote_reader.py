import pandas as pd
import datetime
import matplotlib.pyplot as plt
import talib


def get_datetime(df):
    date = df['data_date']
    time = df['data_time']
    dt = datetime.datetime.strptime(time + " " + date, "%H:%M:%S %Y-%m-%d")
    return dt

f = pd.read_hdf("/Users/klkgogo/histData/Quote_2018-10-08.h5")
# f = f.set_index('data_time')
# st = pd.HDFStore("/Users/lingkunkong/Downloads/Quote_2018-10-08.h5", 'r')
# print(st['data'])
# st.close()
#
# f = pd.read_hdf("/Users/lingkunkong/Downloads/ticker_2018-10-08.h5")
# print(f)
# print(f[f['code'] == 'HK.63257'])
#
# f = pd.read_hdf("Quote_2018-10-08.h5")

def kdj(data, fk, sk, sd):
    pre_addition_num = fk + max(sk, sd)
    delta = data.index[1] - data.index[0]
    pre_addition_index = data.index[:pre_addition_num]
    pre_addition_index = pre_addition_index - delta * pre_addition_num
    print(pre_addition_index)
    pre_addition = pd.DataFrame({'open': data['open'][0], 'high': data['high'][0], 'low': data['low'][0], 'close': data['close'][0]}, index=pre_addition_index)
    data_extend = pre_addition.append(data)
    print(data_extend)
    k, d = talib.STOCH(data_extend['high'], data_extend['low'], data_extend['close'], fastk_period=fk, slowk_period=sk,
                       slowk_matype=1, slowd_period=sd, slowd_matype=1)
    print(k)
    j = 3*k - 2*d
    return k[pre_addition_num:], d[pre_addition_num:], j[pre_addition_num:]


print(f)
# print(f["data_date"])

index = f.apply(get_datetime, axis=1)
f.index = index
start_time = datetime.datetime.strptime("9:30:00" + " " + f['data_date'][0], "%H:%M:%S %Y-%m-%d")
f = f.loc[start_time:]
last_price = f['last_price']
f_resample= last_price.resample('5S', label='right', closed='right').ohlc()
f_resample = f_resample.dropna()
print(f_resample)
print(f_resample[:4520])
# matype: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
#k, d = talib.STOCH(f_resample['high'], f_resample['low'], f_resample['close'], fastk_period=9, slowk_period=3, slowk_matype=5, slowd_period=3, slowd_matype=6) #the best
# k, d = talib.STOCH(f_resample['high'], f_resample['low'], f_resample['close'], fastk_period=50, slowk_period=12, slowk_matype=1, slowd_period=12, slowd_matype=1)
k, d, j = kdj(f_resample, 36, 12, 12)

# #
n = 200
print(k)
print(d)

plt.figure()
# plt.subplot(211)
norm = (f_resample['close'] - f_resample['close'].min()) / (f_resample['close'].max() - f_resample['close'].min()) * 100
norm[:n].plot(grid=True)

# plt.subplot(212)
k[:n].plot(grid=True)
d[:n].plot(grid=True)
j[:n].plot(grid=True)
plt.show()

