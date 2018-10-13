import SampleTicker as st
from futuquant import *
import pandas as pd
import time
import datetime as dt

from smsplugin import Sms

pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)

class StockQuoteHandler(StockQuoteHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(StockQuoteHandler,self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("StockQuoteTest: error, msg: %s" % data)
            return RET_ERROR, data
        print(data)
        content = data[['code', 'data_date', 'data_time', 'last_price']]
        #print(content) # StockQuoteTest自己的处理逻辑

        return RET_OK, data

if __name__ == '__main__':
    context = OpenQuoteContext(host='127.0.0.1', port=11111)
    # context = ft.OpenQuoteContext(host='192.168.56.2', port=11111)
    code = 'HK.800000'
    #code = 'SH.000001'
    quote_handler = StockQuoteHandler()
    context.subscribe([code], [SubType.QUOTE])
    context.set_handler(quote_handler)
    while True:
        time.sleep(10)
