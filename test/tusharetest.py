import tushare as ts
from tushare.stock import cons as ct
from tushare.util import dateu as du
print(ts.__version__)
data = ts.get_hist_data('00700')
symbol = ct._code_to_symbol('600030')
url = ct.DAY_PRICE_URL%(ct.P_TYPE['http'], ct.DOMAINS['ifeng'],
                                ct.K_TYPE['D'], symbol)
print(url)
# print(data)
df= ts.get_tick_data('600030', date='2018-03-02')
print(df)
date = du.today()
print(date)
url = ct.TODAY_TICKS_PAGE_URL % (ct.P_TYPE['http'], ct.DOMAINS['vsf'],
                                                       ct.PAGES['jv'], date,
                                                       symbol)
url = ct.TICK_PRICE_URL % (ct.P_TYPE['http'], ct.DOMAINS['sf'], ct.PAGES['dl'],
                           '2018-03-02', symbol)
print(url)
