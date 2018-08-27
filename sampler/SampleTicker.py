import futuquant as ft
import pandas as pd
import datetime as dt
import time
import socket
import codecs
from futuquant import *

from smsplugin import Sms
from emailplugin import EmailNotification

def genOrderBookColums():
    indexAsk = ['Ask_price' + str(x) for x in range(10)]
    indexAsk_volume = ['Ask_volume' + str(x) for x in range(10)]
    indexAsk_num = ['Ask_num' + str(x) for x in range(10)]

    indexBid = ['Bid_price' + str(x) for x in range(10)][::-1]
    indexBid_volume = ['Bid_volume' + str(x) for x in range(10)][::-1]
    indexBid_num = ['Bid_num' + str(x) for x in range(10)][::-1]
    index = indexBid + indexAsk + indexBid_volume + indexAsk_volume + indexBid_num + indexAsk_num + ['code', 'timestamp']
    return index

def changeOrderBookValueToList(ob):
    valuesAsk = [x[0] for x in ob['Ask']]
    valuesAskV = [x[1] for x in ob['Ask']]
    valuesAskN = [x[2] for x in ob['Ask']]

    valuesBid = [x[0] for x in ob['Bid']][::-1]
    valuesBidV = [x[1] for x in ob['Bid']][::-1]
    valuesBidN = [x[2] for x in ob['Bid']][::-1]
    values = valuesBid + valuesAsk + valuesBidV + valuesAskV + valuesBidN + valuesAskN + [ob['code'] , ob['timestamp']]
    return values

class SamplerBase(object):
    TotalCount = 0

    def __init__(self, name, maxCacheNum = 200):
        self.TotalCount = 0
        self.CacheCount = 0
        self.maxCacheNum = maxCacheNum
        self.CacheData = pd.DataFrame()
        self.day = str(dt.datetime.now())[:10]
        self.name = name

    def sample(self, content):
        self.CacheCount += content.shape[0]
        self.TotalCount += content.shape[0]
        self.CacheData = self.CacheData.append(content)

        if self.CacheCount > self.maxCacheNum:
            self.saveCache(self.CacheData)
            self.clearCache()

    def clearCache(self):
        self.CacheData.drop(self.CacheData.index, inplace=True)
        self.CacheCount = 0

    def saveCache(self, data):
        if (data.shape[0] == 0):
            print(self.name, ": cache empty")
            return
        fileName = self.name + "_" + self.day + ".h5"
        f = pd.HDFStore(fileName, 'a')
        f.put('data', data, format="table", append=True)
        f.close()
        print("save: " + fileName)

    def flush(self):
        self.saveCache(self.CacheData)
        self.clearCache()



class TickerHandler(TickerHandlerBase, SamplerBase):
    def __init__(self):
        SamplerBase.__init__(self, name = "ticker")

    def on_recv_rsp(self, rsp_str):
        print("on_recv_rsp ticker enter")
        ret_code, content = super(TickerHandler,self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了逐笔信息，格式与get_rt_ticker一样
        if ret_code != RET_OK:
            print("TickerTest: error, msg: %s" % content)
            return RET_ERROR, content
        print('tk Count:', self.TotalCount, content[['code', 'time', 'price', 'volume']].values)  # StockQuoteTest自己的处理逻辑
        # print(content)
        self.sample(content)
        print("on_recv_rsp ticker exit")
        return RET_OK, content

class OrderBookHandler(OrderBookHandlerBase, SamplerBase):
    """
    获得摆盘推送数据
    """
    def __init__(self):
        SamplerBase.__init__(self, name = "orderbook")
        self.col = genOrderBookColums()

    def on_recv_rsp(self, rsp_str):
        """数据响应回调函数"""
        print("on_recv_rsp orderbook enter")
        ret_code, content = super(OrderBookHandler, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("OrderBookTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("ob count:", self.TotalCount, content['code'], " Bid:", content['Bid'][0],"ask:", content['Ask'][0])
        # print("ob count:", self.TotalCount)
        # print(content)
        content['timestamp'] = str(dt.datetime.now())
        df = pd.DataFrame([changeOrderBookValueToList(content)], columns=self.col)
        self.sample(df)
        print("on_recv_rsp orderbook exit")
        return RET_OK, content


class StockSampler(object):
    def __init__(self, context):
        self.context = context
        self.tickHandler = TickerHandler()
        self.orderbookHandler = OrderBookHandler()
        self.context.set_handler(self.tickHandler)
        self.context.set_handler(self.orderbookHandler)

    def tickSubscribe(self, stock_code):
        for c in stock_code:
            ret_code, msg = self.context.subscribe(c, [SubType.TICKER])
            if (ret_code == RET_ERROR):
                print(msg, c)

    def orderbookSubscribe(self, stock_code):
        for c in stock_code:
            ret_code, msg = self.context.subscribe(c, [SubType.ORDER_BOOK])
            if (ret_code == RET_ERROR):
                print(msg, c)

    def startSample(self):
        self.context.start()
        # send_msg('Sample start:{}:{}'.format(socket.gethostname(), time.ctime()), 'sample start:{}'.format(time.ctime()))
        Sms.send_start_sample()

    def stopSample(self):
        self.orderbookHandler.flush()
        self.tickHandler.flush()
        print("stop sample, ob count: ", self.orderbookHandler.TotalCount, " tickerCount: ", self.tickHandler.TotalCount)
        # send_msg('Sample end:{}:{}'.format(socket.gethostname(), time.ctime()),
        #          'sample end:{}, tickerCount:{}, orderbookCount:{} '.format(time.ctime(), self.tickHandler.TotalCount, self.orderbookHandler.TotalCount ))
        Sms.send_end_sample(self.orderbookHandler.TotalCount, self.tickHandler.TotalCount)


def getStockList(context):
    """取沪深300股票，沪深各取25只"""
    ret_code, ret_data = context.get_plate_stock("SH.BK0155")
    # print(ret_data['code'].map(lambda x: "SZ" in x))
    sz300 = ret_data[ret_data['code'].map(lambda x: "SZ" in x)]
    sh300 = ret_data[ret_data['code'].map(lambda x: "SH" in x)]
    return sz300[:25].append(sh300[:25])

def getHISStockList(context):
    ret_code, ret_data = context.get_plate_stock("HK.800000")
    return ret_data


def isEnd():
    t = time.localtime()
    min = t.tm_hour * 60 + t.tm_min
    # 下午4点30分
    min_thresh = 16 * 60 + 30
    if min > min_thresh:
        return True
    else:
        return False


def send_msg(subject, words):
    receiver = '49072565@qq.com'
    EmailNotification.set_enable(True)
    EmailNotification.send_email(receiver, subject, words)

if __name__ == '__main__':
    # if sys.stdout.encoding != 'UTF-8':
    #     sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    # if sys.stderr.encoding != 'UTF-8':
    #     sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

    context = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
    stockSampler = StockSampler(context)
    stocklist = getHISStockList(context)
    #print(stocklist)
    print(len(stocklist))
    stockSampler.tickSubscribe(stocklist['code'])
    stockSampler.orderbookSubscribe(stocklist['code'])
    stockSampler.startSample()

    try:
        while 1:
            time.sleep(10)
            if isEnd():
                break
        print("sample end")
    except BaseException as err:
        print("interrupt", err)
        send_msg('Sample end unexpected', 'unexpected end:{0}'.format(err))
        Sms.send_exception(err)
    finally:
        context.close()
        stockSampler.stopSample()
        print(time.ctime())