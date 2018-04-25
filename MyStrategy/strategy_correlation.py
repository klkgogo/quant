from futuquant.open_context import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)


def norm(data, col):
    open = data['open'][0]
    ratio = data['change_rate'][0]
    base = open / (1 + ratio / 100)
    s = data['close']
    ss = pd.Series([base]).append(s)
    return ss / base


def get_cov(code1, plate, start_date = None, end_date = None):
    _, days = quote_ctx.get_trading_days('SZ', start_date, end_date)
    days=days[::-1]
    valid_days =[] #有可能某个交易日停牌，这里保存正常开盘的日子
    ret = []
    print("day count ", len(days))
    for i in range(len(days)):
        date = days[i]
        r, k1m_1 = quote_ctx.get_history_kline(code1, start=date, end=date, ktype="K_1M", autype='qfq')
        _, k1m_2 = quote_ctx.get_history_kline(plate, start=date, end=date, ktype="K_1M", autype='qfq')
        if len(k1m_1['close']) != len(k1m_2['close']):  #若股票某天停牌，返回的数据为空
            ret = ret + [(1, 0)]
            continue
        valid_days = valid_days + [date]
        norm1 = norm(k1m_1, 'close')
        norm2 = norm(k1m_2, 'close')
        cor = norm2.corr(norm1)
        n = len(norm1)
        a = norm1[n -2]
        b = norm2[n-2]
        if (a > b):
            buy_or_sell = 1
        else:
            buy_or_sell = -1
        ret = ret + [(cor, buy_or_sell)]
        print(date, " ", ret[i][0], " ", buy_or_sell)
        if DEBUG and ret[i][0] < THRESH_COV_BUY:
            plt.subplot(2,1,1)
            plt.plot(norm1)
            plt.subplot(2,1,2)
            plt.plot(norm2)
            plt.show()

    return ret, valid_days


def get_stock_kline(stock_code, start=None, end=None):  #停牌的时候用前一个交易日价格替代
    _, days = quote_ctx.get_trading_days('SZ', start_date, end_date)
    days=days[::-1]
    data = pd.DataFrame()
    df = pd.DataFrame()
    for i in range(len(days)):
        date = days[i]
        _, stock_kday = quote_ctx.get_history_kline(stock_code, start=date, end=date, ktype="K_DAY", autype='qfq')
        if len(stock_kday['close']) == 0:
            if df.empty:
                df = pd.DataFrame([[0, 0, days[i]]], columns=['close', 'change_rate', 'date'])
        else:
            df = pd.DataFrame([[stock_kday['close'][0], stock_kday['change_rate'][0], days[i]]], columns=['close', 'change_rate', 'date'])

        if data.empty:
            data = df
        else:
            data = data.append(df)
    # index = [ i for i in range(len(days))]
    # data.set_index(index)
    # data.reset_index(index)
    data.index = range(len(days))
    return data

def get_buy_sell_point(cov, quote, plate):
    points = []
    for i in range(len(cov)):
        buy_or_sell = 0
        if cov[i][1] > 0:
            if cov[i][0] < THRESH_COV_BUY and math.fabs(quote['change_rate'][i]) < 2:
                buy_or_sell = 1
        else:
            if cov[i][0] < THRESH_COV_SELL_1:
                buy_or_sell = -1
                # if plate['change_rate'][i] > 0:  #若大市上涨
                #     buy_or_sell = -2


        # if quote['change_rate'][i] > 0:
        #     if cov[i][0] < THRESH_COV_BUY:
        #         buy_or_sell = 1
        # else:
        #     if cov[i][0] < THRESH_COV_SELL_1:
        #         buy_or_sell = -1
        #         # if plate['change_rate'][i] > 0:  #若大市上涨
        #         #     buy_or_sell = -2

        #
        # if cov[i] < THRESH_COV_BUY:
        #     if quote['change_rate'][i] > 0:
        #         buy_or_sell = 1
        #     else:
        #         buy_or_sell = -1
        # elif cov[i] < THRESH_COV_SELL_1:
        #     if quote['change_rate'][i] < 0
        #         buy_or_sell = -1
        p = (i, quote['close'][i], buy_or_sell, quote['date'][i])
        points = points + [p]
    return points


def backtesting(bs, quote, init_fund):
    n = len(bs)
    state = 0  #持仓状态，1：持仓，0：空仓
    fund = np.zeros(n)
    fund[0] = init_fund
    buy_price = 0
    buy_count = 0
    sell_price = 0
    buy_date  = 0
    sell_date = 0
    win_count = 0
    lost_count = 0
    max_lost = 0
    keep_days = 0
    max_price = 0
    for i in range(n):
        buy = bs[i][2]
        order = 0
        if buy == 1 and state != 1:
            #判断是否涨停
            change_rate = quote['change_rate'][i]
            if change_rate < 9.5:
                buy_price = bs[i][1] #以收盘价买入
                buy_date = bs[i][3]
                if (i == 0):
                    ff = init_fund
                else:
                    ff = fund[i -1]
                buy_count = math.floor(ff / buy_price / 100) * 100
                state = 1
                order = 1
                keep_days = 1
                max_price = buy_price

        # if (buy == -1 or (keep_days == 1 and quote['close'][i] < quote['close'][i-1])) and state == 1 and order != 1:
        # if (buy == -1 or (quote['close'][i] / max_price < 0.95)) and state == 1 and order != 1:
        if buy == -1 and state == 1 :
            if quote['change_rate'][i] > -10:
                sell_price = bs[i][1] #以收盘价卖出
                sell_date = bs[i][3]
                state = 0
                order = -1

         #如果持仓，并且是刚卖出计算持仓收益
        if state == 1 and order !=1: #持仓
            if quote['close'][i] > max_price:
                max_price = quote['close'][i]
            delta = 0
            keep_days += 1
            if (i > 0):
                delta = quote['close'][i] - quote['close'][i-1]
                fund[i] = fund[i - 1] + buy_count * delta
        elif order == -1: #股票卖出
            keep_days = 0
            delta = quote['close'][i] - quote['close'][i - 1]
            fund[i] = fund[i - 1] + buy_count * delta
        else: #没有持有
            if i > 0:
                fund[i] = fund[i-1]

        if sell_price > 0:  #计算收益
            profit = (sell_price - buy_price) * buy_count
            print("buy at: ", buy_date, " price: ", buy_price,
                  " sell at: ", sell_date, " price: ", sell_price,
                  " count:", buy_count,  " profit:", profit,
                  " fund: " , fund[i])
            if profit > 0:
                win_count += 1
            else:
                if profit < max_lost:
                    max_lost = profit
                lost_count += 1
            sell_price = 0  #复位
    print("order cout:", lost_count + win_count, " lost:", lost_count, " win:", win_count, " win rate:", win_count/(win_count + lost_count) * 100, " maxlost:" , max_lost)
    return fund

quote_ctx = OpenQuoteContext(host='192.168.56.2', port=11111)

stock_code = 'SZ.002848'
# stock_code = 'SZ.002806'
# stock_code = 'SZ.300661'
# stock_code = 'SZ.002052'
# stock_code = 'SZ.002759'
# stock_code = 'SZ.002049'
stock_code = 'SZ.002192'

start_date = "2018-01-10"
# start_date = "2017-09-01"

idx_sz = 'SZ.399001'
idx_sh = 'SZ.000001'
idx_cyb = 'SZ.159915'


THRESH_COV_BUY = 0.5
THRESH_COV_SELL_1 = 0.8
THRESH_COV_SELL_2 = 0.8

end_date = None
# end_date = "2018-01-30"
DEBUG = False
# DEBUG = True
# ret, stock_kday = quote_ctx.get_history_kline(stock_code, start=start_date, end=end_date, ktype="K_DAY", autype='qfq')
stock_kday = get_stock_kline(stock_code, start_date, end_date)

ret, sz_kday = quote_ctx.get_history_kline(idx_sz, start=start_date, end=end_date, ktype="K_DAY", autype='qfq')
ret, sh_kday = quote_ctx.get_history_kline(idx_sh, start=start_date, end=end_date, ktype="K_DAY", autype='qfq')
ret, cyb_kday = quote_ctx.get_history_kline(idx_cyb, start=start_date, end=end_date, ktype="K_DAY", autype='qfq')

# stock_kday_close = get_stock_kline(stock_code, start_date, end_date)

# _, k1m_1 = quote_ctx.get_history_kline('SZ.300077', start="2018-04-19", end="2018-04-19", ktype="K_1M", autype='qfq')
# print(k1m_1)
plate = sz_kday

cov, valid_days = get_cov(stock_code, idx_cyb, start_date, end_date)
# print(" cov len:" , len(cov))


bs_point = get_buy_sell_point(cov, stock_kday, plate)

fund = backtesting(bs_point, stock_kday, 100000)
print(" totol fund: " , fund[-1])

### print mat
norm_fund = fund / fund[0] * stock_kday['close'][0] #标准化成和stock_kday一样大，便于比较

index = range(len(cov))
# fig = plt.figure()
# ax = fig.subplots()
locator= MultipleLocator(1)
# ax.xaxis.set_minor_locator(xmajorLocator)
# ax.xaxis.grid(True, which='minor')

plt.close()

ax=plt.subplot(3,1,1)
xmajorLocator= MultipleLocator(1)
ax.xaxis.set_minor_locator(locator)
ax.xaxis.grid(True, which='minor')
plt.title(idx_cyb)
plt.plot(index, cyb_kday['close'])
plt.grid()

ax=plt.subplot(3,1,2)
xmajorLocator= MultipleLocator(1)
ax.xaxis.set_minor_locator(locator)
ax.xaxis.grid(True, which='minor')
plt.title(stock_code)
plt.plot(index, stock_kday['close'])
plt.grid()
for p in bs_point:
    if p[2] == 1:
        plt.plot(p[0],p[1], "r*")
    elif p[2] == -1:
        plt.plot(p[0], p[1], "g*")
    elif p[2] == -2:
        plt.plot(p[0], p[1], "b*")

plt.plot(index, norm_fund, "r")

ax=plt.subplot(3,1,3)
xmajorLocator= MultipleLocator(1)
ax.xaxis.set_minor_locator(locator)
ax.xaxis.grid(True, which='minor')
plt.title("cov")
plt.plot(index, cov)
plt.grid()


quote_ctx.close()
# print(cov)
# print(bs_point)
plt.show()

