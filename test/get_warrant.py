import futuquant as ft
import pandas as pd
import datetime as dt
import time

MAX_SANPSHOT = 200


def get_last_day_turnover_(context, code):
    dt_now = dt.datetime.now()
    # 历史日k取近365天的数据 , 其它k线类型取近30天的数据
    # dt_start = dt_now - timedelta(days= 365 if ktype == KTYPE_DAY else 30)
    dt_start = dt_now - dt.timedelta(days=30)
    str_start = dt_start.strftime("%Y-%m-%d")
    str_end = dt_now.strftime("%Y-%m-%d")
    ret, data = context.get_history_kline(code=code, start=str_start, end=str_end, ktype='K_DAY', autype='qfq')
    turnover = data['turnover'].values
    # print(code)
    # print(turnover)
    if turnover.size == 0:
        return 0
    else:
        return turnover[-1]

def get_last_day_turnover(context, code_list):
    turnover = []
    for code in code_list:
        v = get_last_day_turnover_(context, code)
        turnover.append(v)
    return turnover


def get_warrant_snapshot(context, code):
    """
    获取某正股的涡轮的snapshot, 按前一收市成交量排序
    :param context: QuoteContext
    :param code: 正股代码
    :return: 涡轮列表
    """
    ret_code, ret_data = context.get_stock_basicinfo('HK', 'WARRANT')
    wrt_list = ret_data[ret_data['owner_stock_code'] == code]['code'].values
    if len(wrt_list) == 0:
        print("Error can not get stock info '{}'".format(code))
        return

    # 按频率限制获取股票快照: 每5秒200支股票
    snapshot = pd.DataFrame()
    for i in range(0, len(wrt_list), 200):
        print("from {}, total {}".format(i, len(wrt_list)))
        ret_code, ret_data = quote_ctx.get_market_snapshot(list(wrt_list[i:i + 200]))
        if ret_code != 0:
            print(ret_data)
        snapshot = snapshot.append(ret_data)
        time.sleep(5)

    snapshot = snapshot.sort_values(by='turnover', ascending=False)
    return snapshot


if __name__ == "__main__":
    quote_ctx = ft.OpenQuoteContext(host='192.168.56.2', port=11111)
    # ret_code, ret_data = quote_ctx.get_trading_days(market='HK')
    # print(ret_code, ret_data)
    # ret_code, ret_data = quote_ctx.get_stock_basicinfo(market='HK', stock_type='STOCK')
    # # print(ret_code, ret_data)
    # # print(type(ret_data))

    # ret_code, ret_data = quote_ctx.get_stock_basicinfo('HK', 'WARRANT')
    # tc_wrt = ret_data[ret_data['owner_stock_code'] == 'HK.00700']
    # print(tc_wrt)
    # snapshot = pd.DataFrame()
    # code_list = tc_wrt['code'].values
    # count = len(code_list)
    # l = range(MAX_SANPSHOT, count, MAX_SANPSHOT)
    # print(list(l))
    # for stop_index in range(MAX_SANPSHOT, count, MAX_SANPSHOT):
    #     print("%d:%d" % (stop_index - MAX_SANPSHOT, stop_index))
    #     sub_code_list = code_list[stop_index - MAX_SANPSHOT:stop_index]
    #     print(sub_code_list)
    #     ret_code, ret_data = quote_ctx.get_market_snapshot(list(sub_code_list))
    #     snapshot = snapshot.append(ret_data)
    #     time.sleep(6)
    #     # break
    #
    # print("%d:%d" % (stop_index, count))
    # sub_code_list = code_list[stop_index:count]
    # ret_code, ret_data = quote_ctx.get_market_snapshot(list(sub_code_list))
    # snapshot = snapshot.append(ret_data)
    #
    # # turnover = get_last_day_turnover(quote_ctx, code_list)
    # # print(turnover)
    # # snapshot['turnover'] = turnover

    # snapshot = snapshot.sort_values(by='turnover', ascending=False)
    snapshot = get_warrant_snapshot(quote_ctx, "HK.00700")
    print(snapshot[snapshot['turnover'] > 0])
    call = snapshot[snapshot['wrt_type'] == 'CALL']
    put = snapshot[snapshot['wrt_type'] == 'PUT']
    bull = snapshot[snapshot['wrt_type'] == 'BULL']
    bear = snapshot[snapshot['wrt_type'] == 'BEAR']
    print(call)
    quote_ctx.close()