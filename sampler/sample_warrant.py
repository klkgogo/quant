import SampleTicker as st
import futuquant as ft
import pandas as pd
import time
import datetime as dt

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
        ret_code, ret_data = context.get_market_snapshot(list(wrt_list[i:i + 200]))
        if ret_code != 0:
            print(ret_data)
        snapshot = snapshot.append(ret_data)
        time.sleep(5)

    snapshot = snapshot.sort_values(by='turnover', ascending=False)
    return snapshot

def get_sample_warrant(context, code):
    """
    获取要采集的涡轮，call, put, bull, bear轮按成交量排行，各取前NUM_SAMPLE只
    :param context:
    :param code: 要采集的涡轮正股
    :return:
    """
    NUM_SAMPLE = 40  # 每种涡轮采集的数量
    snapshot = get_warrant_snapshot(context, code)
    call = snapshot[snapshot['wrt_type'] == 'CALL']
    put = snapshot[snapshot['wrt_type'] == 'PUT']
    bull = snapshot[snapshot['wrt_type'] == 'BULL']
    bear = snapshot[snapshot['wrt_type'] == 'BEAR']
    if (call.shape[0] > NUM_SAMPLE):
        call = call[0:NUM_SAMPLE]
    if (put.shape[0] > NUM_SAMPLE):
        put = put[0:NUM_SAMPLE]
    if (bull.shape[0] > NUM_SAMPLE):
        bull = bull[0:NUM_SAMPLE]
    if (bear.shape[0] > NUM_SAMPLE):
        bear = bear[0:NUM_SAMPLE]

    sample_list = call
    sample_list = sample_list.append(put)
    sample_list = sample_list.append(bull)
    sample_list = sample_list.append(bear)
    return sample_list

if __name__ == '__main__':
    context = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
    # context = ft.OpenQuoteContext(host='192.168.56.2', port=11111)
    code = 'HK.00700'
    stockSampler = st.StockSampler(context)
    warrant_snapshot = get_sample_warrant(context, code)

    str_day = str(dt.datetime.now())[:10]
    fileName = "orderbook_" + str_day + ".h5"
    f = pd.HDFStore(fileName, 'a')
    f['warrant_info'] = warrant_snapshot
    f.close()

    stockSampler.tickSubscribe([code])
    stockSampler.orderbookSubscribe([code])
    stockSampler.orderbookSubscribe(warrant_snapshot['code'])
    stockSampler.startSample()

    try:
        while 1:
            time.sleep(10)
            if st.isEnd():
                break
        print("sample end")
    except BaseException:
        print("interrupt")
        st.send_msg('自动采集程序结束:异常终止', '异常终止')
    finally:
        context.close()
        stockSampler.stopSample()
        print(time.ctime())