from futuquant.open_context import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import SinaStockAccount.stock_account as sa
import math
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

pd.set_option('display.max_rows',None)
MAX_NUM = 120
def norm(data, col):
    base = data['open'][0]
    s = data['close']
    ss = pd.Series([base]).append(s)
    return ss / base

def get_cur_k1m(context, code):
    # 获取当天的1M k线
    context.subscribe(code, 'K_1M')
    ret_err, ret_data = context.get_cur_kline(code, num=MAX_NUM + 1, ktype="K_1M", autype='qfq')
    _, ret = context.unsubscribe(code, 'K_1M')
    return ret_err, ret_data


def get_plate_stock_list(context, plate):
    """或取板块下的股票"""
    ret_code, ret_data = context.get_plate_stock(plate)
    return ret_data

def get_plate_cor(context, stock_plate):
    """计算板块下的股票和板块指数的相关性"""
    stock_list = get_plate_stock_list(context, stock_plate)
    df = pd.DataFrame(stock_list['code'])
    df['stock_name'] = stock_list['stock_name']
    df['cor'] = 0

    err, plate_k1m = get_cur_k1m(context, stock_plate)
    norm_plate = norm(plate_k1m, 'close')
    open = plate_k1m['open'][0]
    close = plate_k1m['close'][MAX_NUM]
    plate_change_rate = (close - open) / open * 100
    print("plate change rate: ", plate_change_rate)

    count = df.shape[0]
    change_rate = np.zeros(count)
    cor = np.zeros(count)
    factor = np.zeros(count)
    delta = np.zeros(count)
    for i in range(count):
        code = df['code'][i]
        print(code)
        err, k1m = get_cur_k1m(context, code)
        if err != RET_OK:
            print(code, k1m)
            continue
        change_rate[i] = (k1m['close'][MAX_NUM] - k1m['open'][0]) / k1m['open'][0] * 100
        factor[i] = change_rate[i] / plate_change_rate
        delta[i] = change_rate[i] - plate_change_rate
        norm_code = norm(k1m, 'close')
        cor[i] = norm_code.corr(norm_plate)
    df['cor'] = cor
    df['change_rate'] = change_rate
    df['factor'] = factor
    df['delta'] = delta
    return df

if __name__ == '__main__':
    STOCK_PLATE = 'SZ.399005'
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    stock_list = get_plate_cor(quote_ctx, STOCK_PLATE)
    stock_list = stock_list.sort_values(by='cor')
    f1 = stock_list[stock_list['cor'] < 0.6]
    f2 = f1[f1["delta"] > 0]
    print(stock_list)

    print(f1)
    print(f2)
    print("f1 count: %d, f2 count: %d" %( f1.shape[0], f2.shape[0]))

    # 添加到sina 我的账本 http://i.finance.sina.com.cn/zixuan,stock
    date = time.strftime("%m-%d", time.localtime())
    group1 = date + "_f1"
    group2 = date + "_f2"
    sa.add_to_sina_account(group1, f1)
    sa.add_to_sina_account(group2, f2)
    # _, pid = sa.create_group(group2)
    # for ix, row in f2.iterrows():
    #     print(ix)
    #     sa.add_stock(pid, sa.futu_to_sina_code(row['code']))

    quote_ctx.close()