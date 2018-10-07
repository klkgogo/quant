import SampleTicker as st
from futuquant import *
import pandas as pd
import time
import datetime as dt

from smsplugin import Sms

def get_warrant_snapshot(context, code):
    """
    获取某正股的涡轮的snapshot, 按前一收市成交量排序
    :param context: QuoteContext
    :param code: 正股代码
    :return: 涡轮列表
    """
    ret_code, ret_data = context.get_stock_basicinfo(Market.HK, SecurityType.WARRANT)
    wrt_list = ret_data[ret_data['stock_owner'] == code]['code'].values
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
    NUM_SAMPLE = 80  # 每种涡轮采集的数量
    snapshot = get_warrant_snapshot(context, code)
    bull = snapshot[snapshot['wrt_type'] == 'BULL']
    bear = snapshot[snapshot['wrt_type'] == 'BEAR']
    # if (call.shape[0] > NUM_SAMPLE):
    #     call = call[0:NUM_SAMPLE]
    # if (put.shape[0] > NUM_SAMPLE):
    #     put = put[0:NUM_SAMPLE]
    if (bull.shape[0] > NUM_SAMPLE):
        bull = bull[0:NUM_SAMPLE]
    if (bear.shape[0] > NUM_SAMPLE):
        bear = bear[0:NUM_SAMPLE]

    # sample_list = call
    # sample_list = sample_list.append(put)
    # sample_list = sample_list.append(bull)
    # sample_list = sample_list.append(bear)
    sample_list = bull
    sample_list = sample_list.append(bear)
    return sample_list


class SamplerBase(object):
    TotalCount = 0

    def __init__(self, name, maxCacheNum = 200):
        self.TotalCount = 0
        self.CacheCount = 0
        self.maxCacheNum = maxCacheNum
        self.CacheData = pd.DataFrame()
        self.day = str(dt.datetime.now())[:10]
        self.name = name
        self.fileName = self.name + "_" + self.day + ".h5"
        self.f = pd.HDFStore(self.fileName, 'a')

    def sample(self, content):
        self.CacheCount += content.shape[0]
        self.TotalCount += content.shape[0]
        self.CacheData = self.CacheData.append(content)

        if self.CacheCount > self.maxCacheNum:
            self.saveCache(self.CacheData)
            self.clearCache()

    def clearCache(self):
        #self.CacheData.drop(self.CacheData.index, inplace=True)
        self.CacheData = pd.DataFrame()
        self.CacheCount = 0

    def saveCache(self, data):
        if (data.shape[0] == 0):
            print(self.name, ": cache empty")
            return
        self.f.put('data', data, format="table", append=True)
        self.f.flush()
        print("save: " + self.fileName)

    def flush(self):
        self.saveCache(self.CacheData)
        self.clearCache()

    def stop(self):
        self.f.close()



class StockQuoteHandler(StockQuoteHandlerBase, SamplerBase):
    def __init__(self):
        SamplerBase.__init__(self, name = "Quote")

    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(StockQuoteHandler,self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("StockQuoteTest: error, msg: %s" % data)
            return RET_ERROR, data
        content = data[['code', 'data_date', 'data_time', 'last_price']]
        self.sample(content)
        print("StockQuoteTest ", content) # StockQuoteTest自己的处理逻辑

        return RET_OK, data

if __name__ == '__main__':
    context = OpenQuoteContext(host='127.0.0.1', port=11111)
    # context = ft.OpenQuoteContext(host='192.168.56.2', port=11111)
    code = 'HK.800000'
    stockSampler = st.StockSampler(context)
    warrant_snapshot = get_sample_warrant(context, code)

    str_day = str(dt.datetime.now())[:10]
    fileName = "orderbook_" + str_day + ".h5"
    f = pd.HDFStore(fileName, 'a')
    f['warrant_info'] = warrant_snapshot
    f.close()
    print(warrant_snapshot)
    quote_handler = StockQuoteHandler()
    context.set_handler(quote_handler)
    context.subscribe([code], [SubType.QUOTE])
    # stockSampler.tickSubscribe([code])
    stockSampler.tickSubscribe(warrant_snapshot['code'])
    stockSampler.orderbookSubscribe([code])
    stockSampler.orderbookSubscribe(warrant_snapshot['code'])
    stockSampler.startSample()

    try:
        while 1:
            time.sleep(10)
            if st.isEnd():
                break
        print("sample end")
    except BaseException as err:
        print("interrupt, {0}".format(err))
        st.send_msg('Sample end unexpected', 'unexpected,{0}'.format(err))
        Sms.send_exception(err)
    finally:
        context.close()
        stockSampler.stopSample()
        quote_handler.flush()
        quote_handler.stop()
        print(time.ctime())