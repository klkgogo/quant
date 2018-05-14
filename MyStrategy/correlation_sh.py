from correlation_filter import *

from futuquant.open_context import *
import time
import SinaStockAccount.stock_account as sa

STOCK_PLATE = 'SH.000001'
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

stock_list = get_plate_cor(quote_ctx, STOCK_PLATE)
stock_list = stock_list.sort_values(by='cor')
f1 = stock_list[stock_list['cor'] < 0.6]
f2 = f1[f1["delta"] > 0]
print(stock_list)

print(f1)
print(f2)
print("f1 count: %d, f2 count: %d" % (f1.shape[0], f2.shape[0]))

# 添加到sina 我的账本 http://i.finance.sina.com.cn/zixuan,stock
date = time.strftime("%m-%d", time.localtime())
group1 = date + "sh_f1"
group2 = date + "sh_f2"
sa.add_to_sina_account(group1, f1)
sa.add_to_sina_account(group2, f2)
# _, pid = sa.create_group(group2)
# for ix, row in f2.iterrows():
#     print(ix)
#     sa.add_stock(pid, sa.futu_to_sina_code(row['code']))

quote_ctx.close()