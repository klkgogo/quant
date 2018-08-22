from futuquant.open_context import *

quote_ctx = OpenQuoteContext(host='192.168.56.2', port=11111)
ret_code, ret_data = quote_ctx.get_trading_days(market='HK')
print(ret_code, ret_data)
ret_code, ret_data = quote_ctx.get_stock_basicinfo(market='HK', stock_type='STOCK')
print(ret_code, ret_data)
# print(type(ret_data))

ret_code, ret_data = quote_ctx.get_plate_stock('HK', 'HK.00700')
# print(ret_data)
quote_ctx.close();