from futuquant import *
import  time
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
# ret, data, page_req_key = quote_ctx.request_history_kline('HK.800000',  ktype=KLType.K_1M, start='2017-06-20', end='2018-06-22', max_count=50) #请求开头50个数据
# print(ret, data)
for i in range(0, 100):
    ret, snap = quote_ctx.get_market_snapshot(['HK.800000'])

    print(ret, snap['last_price'])
    time.sleep(1.5)

quote_ctx.close()