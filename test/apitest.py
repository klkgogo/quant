from futuquant.open_context import *
from pandas import DataFrame, Series
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
from matplotlib.finance import candlestick2_ochl

quote_ctx = OpenQuoteContext(host='192.168.56.2', port=11111)
ret_code, ret_data = quote_ctx.get_trading_days(market='HK')
print(ret_code, ret_data)
ret_code, ret_data = quote_ctx.get_stock_basicinfo(market='HK', stock_type='STOCK')
# print(ret_code, ret_data)
# print(type(ret_data))



def sum_rate(change_rate):
    ret= np.zeros(change_rate.shape[0])
    trend_start_idx = 0
    trend_start_val = - change_rate[0]
    for i in range(ret.size):
        if trend_start_val * change_rate[i] < 0:
            trend_start_idx = i
            trend_start_val = change_rate[i]
        ret[i] = change_rate[trend_start_idx:i + 1].sum()
    return ret


def trade(data):
    last_buy = 0
    change_thresh = -0.5
    total_earn = 0
    last_buy_idx = 0
    buy_flag = np.zeros(data.shape[0])
    for i in range(data.shape[0]):
        if data['sum_rate'][i] > 0 and data['sum_rate'][i-1] < change_thresh:
            last_buy = data['close'][i]
            last_buy_idx = i;
            print("buy: ", last_buy)

        if last_buy > 0 and data['sum_rate'][i] < 0:
            earn = data['close'][i] - last_buy
            total_earn = total_earn + earn
            print("----buy: ", last_buy, "sell:", data['close'][i], " earn: ", earn, " totalearn: ", total_earn )
            print("----buy_idx: ", last_buy_idx, " sell idx: ",  i )
            last_buy = 0

        if (last_buy > 0):
            buy_flag[i] = 1;

    return (buy_flag, total_earn)


def runTrade(code, start_date):
    ret_code, trading_date = quote_ctx.get_trading_days(market='HK', start=start_date)
    total_earn = 0;
    for date in trading_date:
        ret_code, ret_data = quote_ctx.get_history_kline(code=code, ktype='K_1M', start=date, end=date)
        print("running: ", date)
        data = ret_data.set_index('time_key')[['close', 'change_rate']]
        data['sum_rate'] = sum_rate(data['change_rate'])
        buy_flag, earn = trade(data)
        total_earn = total_earn + earn
        data['buy_flag'] = buy_flag
        print("end running ", date, " earn: ", earn, " total: ", total_earn)


start_date = '2018-01-02'
ret_code, ret_data = quote_ctx.get_history_kline(code='HK.00700', ktype='K_1M', start=date, end=date)
# ret_code, ret_data = quote_ctx.get_history_kline(code='HK.00700', start='2018-01-01')
print(ret_code, ret_data)
data = ret_data.set_index('time_key')[['close', 'change_rate']]

ret_code, trading_date = quote_ctx.get_trading_days(market='HK', start=start_date)
data['sum_rate'] = sum_rate(data['change_rate'])
# print(sum_rate)
print(data)

buy_flag, total_earn = trade(data)
data['buy_flag'] = buy_flag

plt.subplot(3,1,1)
data['close'].plot()
# plt.figure()
# plt.axes([0, data.shape[0], -2, 2])
plt.subplot(3,1,2)
data['sum_rate'].plot()
plt.subplot(3,1,3)
data['buy_flag'].plot()

plt.show()
quote_ctx.close()



# print([0] + ratio)



