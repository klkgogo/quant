from futuquant.open_context import *
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.finance import candlestick2_ochl, candlestick_ochl
from matplotlib.dates import date2num
from datetime import datetime
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY

def getQuotes():
    quote_ctx = OpenQuoteContext(host='192.168.56.2', port=11111)
    # ret_code, ret_data = quote_ctx.get_history_kline(code='HK.00700', ktype='K_1M', start='2018-01-01')
    ret_code, ret_data = quote_ctx.get_history_kline(code='HK.00700', start='2018-01-01')
    quote_ctx.close()
    return ret_data

quotes = getQuotes()
print(type(quotes))
# print(quotes)
quotes = quotes[['time_key', 'open', 'close', 'high', 'low']]

quotes['time'] =quotes['time_key'].map(lambda x: date2num(datetime.strptime(x, "%Y-%m-%d %H:%M:%S")))
# quotes.drop('time_key')
print(quotes)
fig = plt.figure(facecolor='#07000d')
ax = fig.subplots()
ax.set_facecolor('black')
ax.spines['bottom'].set_color("#5998ff")
ax.spines['top'].set_color("#5998ff")
ax.spines['left'].set_color("#5998ff")
ax.spines['right'].set_color("#5998ff")
ax.tick_params(axis='y', colors='w')
ax.tick_params(axis='x', colors='w')
ax.xaxis.label.set_color('w')
ax.yaxis.label.set_color('w')
print(type(quotes['open']))
fig.subplots_adjust(bottom=0.2)
q = DataFrame()
q['time'] =quotes['time_key'].map(lambda x: date2num(datetime.strptime(x, "%Y-%m-%d %H:%M:%S")))
q['open'] = quotes['open']
q['close'] = quotes['close']
q['high'] = quotes['high']
q['low'] = quotes['low']
# print(q)
print(q.values)
# print(quotes)
# print(type(time))
# dtstr = time[0]
# time = [datetime.strptime(t, "%Y-%m-%d %H:%M:%S") for t in time]
# print(time)
# timenum = [date2num(d) for d in time]
# print(timenum)
# print(type(timenum))
# print(date2num(dt))
# print(date2num(time[0]))
# candlestick2_ochl(ax, quotes['open'],quotes['close'], quotes['high'], quotes['low'], width=0.6, colordown='g', colorup='r')
# 设置主要刻度和显示格式
mondays = WeekdayLocator(MONDAY)
mondaysFormatter = DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_major_formatter(mondaysFormatter)

# 设置次要刻度和显示格式
alldays = DayLocator()
alldaysFormatter = DateFormatter('%d')
ax.xaxis.set_minor_locator(alldays)
# ax.xaxis.set_minor_formatter(alldaysFormatter)

#设置x轴为日期
ax.xaxis_date()
ax.autoscale_view()
#X轴刻度文字倾斜45度
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

candlestick_ochl(ax, q.values, width=0.6, colordown='g', colorup='r')
ax.grid(True, color='w')
plt.show()
