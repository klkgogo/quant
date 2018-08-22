from futuquant.open_context import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

quote_ctx = OpenQuoteContext(host='192.168.56.2', port=11111)

def calc_rate(change_rate):
    rate_sum = np.zeros(change_rate.shape[0])
    rate_sum_slow = np.zeros(change_rate.shape[0])
    rate_avg = np.zeros(change_rate.shape[0])
    trend_count = np.zeros(change_rate.shape[0])
    trend_start_idx = 0
    trend_start_idx_slow = 0
    trend_start_val = - change_rate[0]
    trend_start_val_slow = trend_start_val

    for i in range(rate_sum.size):
        if trend_start_val * change_rate[i] < 0:
            trend_start_idx = i
            trend_start_val = change_rate[i]
            trend_count[i] = 0
        elif i > 0:
            if change_rate[i] < 0:
                trend_count[i] = trend_count[i - 1] - 1
            elif change_rate[i] > 0:
                trend_count[i] = trend_count[i - 1] + 1



        rate_sum[i] = change_rate[trend_start_idx:i + 1].sum()

        # if trend_start_val_slow * trend_count[i] < 0:
        if i > 0 and math.fabs(rate_sum[i] / rate_sum_slow[i - 1]) > 0.15 and trend_start_val_slow * trend_count[i] < 0:
            trend_start_idx_slow = trend_start_idx
            trend_start_val_slow = trend_start_val

        rate_sum_slow[i] = change_rate[trend_start_idx_slow:i+1].sum()
        rate_avg[i] = rate_sum[i] / (i - trend_start_idx + 1)
    return rate_sum, rate_avg, trend_count, rate_sum_slow


def min_trend_strage(data, debug=False, buy_thresh=-3, sell_thresh=-0.3):
    last_buy = 0
    change_thresh = buy_thresh
    avg_change_thresh = -0.1
    sell_thresh = sell_thresh
    total_earn = 0
    last_buy_idx = 0
    money = 100000
    stock_count = int(math.floor(money / data['close'][0] / 100)) * 100
    print("stock_count:", stock_count )
    fee = 30;
    total_fee = 0;
    order_count = 0;
    win_count = 0;
    lost_count = 0;
    if debug:
        buy_flag = np.zeros(data.shape[0])
        earn_list = np.zeros(data.shape[0])
    sum_rate, rate_avg, trend_count, sum_rate_slow = calc_rate(data['change_rate'])
    data['sum_rate'] = sum_rate
    data['rate_avg'] = rate_avg
    data['trend_count'] = trend_count
    data['sum_rate_slow'] = sum_rate_slow
    data['idx'] = range(data.shape[0])
    max_price = 0
    change_to_max = 0

    for i in range(data.shape[0]):
        if last_buy == 0 and i > 0:
        # if True:
        #     if data['sum_rate'][i] > 0 and data['sum_rate'][i-1] < change_thresh and data['rate_avg'][i-1] < avg_change_thresh :
        #     if data['sum_rate'][i] > 0 and data['sum_rate'][i - 1] < change_thresh:
        #     if data['sum_rate'][i] > 0 and (data['sum_rate'][i - 1] < change_thresh or data['sum_rate_slow'][i - 1] < change_thresh):
            if data['sum_rate'][i] > 0 and data['sum_rate_slow'][i] < 0 and (data['sum_rate'][i - 1] < change_thresh or data['sum_rate_slow'][i - 1] < change_thresh) and data['rate_avg'][i-1] < avg_change_thresh :

                last_buy = data['close'][i]
                last_buy_idx = i
                order_count += 1
                max_price = last_buy
            # sell_thresh = data['sum_rate'][i-1] /
            sell_thresh = data['sum_rate_slow'][i - 1] / DIVIDE_FACTOR

        # print("buy: ", last_buy)

        if last_buy > 0 and max_price < data['close'][i] and max_price > 0:
            max_price = data['close'][i]


        if (max_price > 0):
            change_to_max = (data['close'][i] - max_price) / max_price
            # print("change to max:", change_to_max, " sell_thresh: ", sell_thresh)

        # if last_buy > 0 and data['sum_rate'][i] < sell_thresh:
        if last_buy > 0 and (change_to_max < sell_thresh or i == (data.shape[0] - 1)):
            earn = data['close'][i] * stock_count - last_buy * stock_count
            if debug:
                earn_list[i] = earn
            total_earn = total_earn + earn
            total_fee = total_fee + fee
            if (earn > 0):
                win_count += 1
            else:
                lost_count += 1
            print("----buy: ", last_buy, "sell:", data['close'][i], " earn: ", earn, " totalearn: ", total_earn )
            print("----buy_idx: ", last_buy_idx, " sell idx: ",  i, " sell thresh: ", sell_thresh)
            last_buy = 0
            max_price = 0
            change_to_max = 0


        if debug and last_buy > 0:
            buy_flag[i] = 1

    if debug and order_count > 0:
    # if debug:
    # if debug:
        print(data[:])
        plt.subplot(3, 1, 1).set_ylim(min(data['close']), max(data['close']))
        data['close'].plot()
        plt.plot(buy_flag * max(data['close']))
        plt.subplot(3, 1, 2)
        data['sum_rate'].plot()
        # print(" earn: ", earn[i], " fee: ", f, " total: ", total_earn)
        plt.subplot(3, 1, 3)
        # plt.plot(earn_list)
        data['sum_rate_slow'].plot()
        plt.show()
    return ( total_earn, total_fee, order_count, win_count, lost_count)



def run_min_starge(code, start_date, end_date= None, debug = False, buy_thresh = -3, sell_thresh = -0.3):
    ret_code, trading_date = quote_ctx.get_trading_days(market='HK', start_date=start_date, end_date=end_date)
    total_earn = 0
    trading_date = trading_date[::-1]
    print(trading_date)
    print(len(trading_date))
    earn = np.zeros(len(trading_date))
    fee = np.zeros(len(trading_date))
    base = np.zeros(len(trading_date))
    order_count = 0
    win_count = 0
    lost_count = 0
    for i in range(len(trading_date)):
        date = trading_date[i]
        ret_code, ret_data = quote_ctx.get_history_kline(code=code, ktype='K_1M', start=date, end=date)
        print("running: ", date)
        if ret_data.shape[0] == 0:
            continue
        data = ret_data.set_index('time_key')[['open', 'close', 'change_rate']]
        # print(data)
        e, f, oc, wc, lc = min_trend_strage(data, debug=debug, buy_thresh= buy_thresh, sell_thresh=sell_thresh)
        earn[i] = e
        fee[i] = f
        base[i] = data['close'][-1]
        total_earn = total_earn + earn[i]
        order_count += oc
        win_count += wc
        lost_count += lc
        print("end running ", date, " earn: ", earn[i],  " fee: " , f, " total: ", total_earn)
        print("")

    df = pd.DataFrame(index = trading_date)
    df['earn'] = earn
    df['fee'] = fee
    df['base'] = base
    return df, order_count, win_count, lost_count


# start_date = '2018-05-17'
start_date = '2018-01-01'
# start_date = '2017-12-06'

DIVIDE_FACTOR = 1000
#
# stock_code = 'HK.00175'
# buy_thresh = -3
# sell_thresh = -0.003


# stock_code = 'HK.02318'
# buy_thresh = -2
# sell_thresh = -0.003
# # #
stock_code = 'HK.00700'
buy_thresh = -1.5
sell_thresh = -0.003

# ret_data, order, win, lost = run_min_starge(stock_code, start_date, debug=False, buy_thresh=buy_thresh, sell_thresh=sell_thresh)
ret_data, order, win, lost = run_min_starge(stock_code, start_date, debug=True, buy_thresh=buy_thresh, sell_thresh=sell_thresh)

quote_ctx.close()


print(ret_data)
total_earn = sum(ret_data['earn']);
total_fee = sum(ret_data['fee'])
print("total ", total_earn, " fee: ", total_fee)
print("total with fee", total_earn - total_fee)
ret_data['earn_with_fee'] = ret_data['earn'] - ret_data['fee']
ret_data['sum_earn_with_fee'] = [ret_data['earn_with_fee'][:i].sum() for i in range(len(ret_data['earn']))]

print("order count: ", order, " win rate: ", win / order * 100, " lost rate: ", lost / order * 100)

win_date = ret_data[ret_data['earn'] > 0]
lost_date = ret_data[ret_data['earn'] < 0]
print(win_date.index)
print(lost_date.index)

plt.subplot(2, 1, 1)
plt.plot(ret_data['base'])
plt.subplot(2, 1, 2)
plt.plot(ret_data['sum_earn_with_fee'])
plt.show()





# print([0] + ratio)



