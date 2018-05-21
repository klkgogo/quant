# encoding: UTF-8

'''
    实盘策略范例，接口用法见注释及范例代码
'''
import talib
from TinyStrateBase import *
import pandas as pd
from MyLib import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from PlotLib import *
import math
import datetime as dt
COLUMNS=['close', 'change_ratio', 'accumulate_change_ratio', 'up_down_count', 'smooth_accumulate_change_ratio']

SMOOTH_THRESH = 0.3
BUY_THRESH = -3


class ReboundStrateWarrant(TinyStrateBase):
    """策略名称, setting.json中作为该策略配置的key"""
    name = 'rebound_strate'

    """策略需要用到行情数据的股票池"""
    symbol_pools = ['HK.00700', 'HK.00175']
    # symbol_pools = ['HK.00175', 'HK.00700']
    # symbol_pools = ['HK.00700']
    # params_pools = {'HK.00700': {'buy_thresh' : -1, 'smooth_buy_thresh' : -1.5 ,'sell_thresh': -0.3, 'dyn_thresh_factor':5,'lot_size':100}
    #           ,'HK.00175': {'buy_thresh' : -2, 'smooth_buy_thresh' : -2, 'sell_thresh': -0.3, 'dyn_thresh_factor':12, 'lot_size':1000} }
    # symbol_pools = ['US.FB', 'US.BABA']

    params_pools = {
        'HK.00700': {'buy_thresh': -0.5, 'smooth_buy_thresh': -0.5, 'sell_thresh': -0.3, 'dyn_thresh_factor': 10,
                     'lot_size': 100, 'war_call': 'HK.11343', 'call_vol': 100000, 'war_put': 'HK.12457', 'put_vol': 100000}
        , 'HK.00175': {'buy_thresh': -1, 'smooth_buy_thresh': -1, 'sell_thresh': -0.3, 'dyn_thresh_factor': 12,
                       'lot_size': 1000, 'war_call': 'HK.12734', 'call_vol': 100000, 'war_put': 'HK.12457', 'put_vol': 100000}}


    def __init__(self):
       super(ReboundStrate, self).__init__()

       """请在setting.json中配置参数"""
       self.param1 = None
       self.param2 = None
       self.cache_data={}
       self.last_am_count={}
       self.buying_list={}
       self.selling_list={}
       self.position_list={}        #持仓信息
       self.highest_track={}        #高点跟踪
       self.trade_history={}

    def on_init_strate(self):
        """策略加载完配置"""
        self.log("on_init_strate")
        # am = self.get_kl_min1_am('HK.00700')
        # self.log(am.close)

    def on_start(self):
        """策略启动入口"""
        self.log("on_start param1=%s param2=%s" %(self.param1, self.param2))

        power = self.get_power()
        """初始化数据"""
        for symbol in self.symbol_pools:
            self.cache_data[symbol] = pd.DataFrame()
            self.last_am_count[symbol] = 0
            self.highest_track[symbol] = 0
            self.trade_history = dict()

        """交易接口测试
        ret, data = self.buy(4.60, 1000, 'HK.03883')
        if 0 == ret:
            order_id = data
            ret, data = self.get_tiny_trade_order(order_id)
            if 0 == ret:
                str_info = ''
                for key in data.__dict__.keys():
                    str_info += "%s='%s' " % (key, data.__dict__[key])
                self.log str_info

        ret, data = self.sell(11.4, 1000, 'HK.01357')
        if 0 == ret:
            order_id = data
            self.cancel_order(order_id)
        """

    def on_quote_changed(self, tiny_quote):
        """报价、摆盘实时数据变化时，会触发该回调"""
        # TinyQuoteData
        data = tiny_quote
        symbol = data.symbol
        # last_price = self.get_last_price('HK.11343')
        if symbol not in self.position_list.keys():
            return
        str_dt = data.datetime.strftime("%Y%m%d %H:%M:%S")
        if data.lastPrice > self.highest_track[symbol]:
            self.highest_track[symbol] = data.lastPrice

        bar = TinyBarData()
        bar.symbol = data.symbol
        bar.open = data.lastPrice
        bar.close = data.lastPrice
        bar.low = data.lastPrice
        bar.volume = 0
        bar.datetime = data.datetime
        self.sell_impl(bar)
        self.log("%s %s %.2f" % (str_dt, bar.symbol, bar.open))

    def on_bar_min1(self, tiny_bar):
        """每一分钟触发一次回调"""
        bar = tiny_bar
        symbol = bar.symbol
        str_dt = bar.datetime.strftime("%H:%M:%S")
        str_now = dt.datetime.now().strftime("%H:%M:%S")
        params = self.params_pools[symbol]
        self.buy(0, 100000, params['target'], order_type=1)  # 竞价单

        # 计算策略指标
        self.calc_index(tiny_bar)

        am = self.get_kl_min1_am(symbol)
        close = am.close[-1]
        str_log = "on_bar_min1 symbol=%s dt=%s open=%s high=%s close=%s  am.close=%s, low=%s vol=%s, count=%s" % (
            symbol, str_dt, bar.open, bar.high, bar.close, close, bar.low, bar.volume, am.count)
        # if close != bar.close:
        #     self.log(str_log)
        # self.log(str_log)
        self.log(str_log)
        self.log(str(am.close[-10:]))
        self.log("generate time: %s, process time:%s" % (str_dt, str_now))
        self.check_position(tiny_bar)
        self.buy_impl(tiny_bar)
        self.sell_impl(tiny_bar)


    def on_bar_day(self, tiny_bar):
        """收盘时会触发一次日k回调"""
        bar = tiny_bar
        symbol = bar.symbol
        str_dt = bar.datetime.strftime("%Y%m%d %H:%M:%S")
        str_log = "on_bar_day symbol=%s dt=%s  open=%s high=%s close=%s low=%s vol=%s" % (
            symbol, str_dt, bar.open, bar.high, bar.close, bar.low, bar.volume)
        self.log(str_log)

    def on_before_trading(self, date_time):
        """开盘时触发一次回调, 港股是09:30:00"""
        str_log = "on_before_trading - %s" % date_time.strftime('%Y-%m-%d %H:%M:%S')
        self.log(str_log)
        for s in self.symbol_pools:
            am = self.get_kl_min1_am(s)
            if am is None:
                continue
            df = pd.DataFrame(am.close[am.size - am.count:].copy(), columns=['close'])
            ratio = change_ratio(am.close[am.size - am.count:])
            ratio = [0] + ratio
            df['change_ratio'] = ratio
            ar = accumulate_ratio(ratio)
            df['accumulate_change_ratio'] = ar
            udc = up_down_count(ratio)
            df['up_down_count'] = udc
            sar = smooth_accumulate_ratio(ratio, ar, udc, SMOOTH_THRESH)
            df['smooth_accumulate_change_ratio'] = sar
            # plt.subplot(3,1,1)
            # plt.plot(df['close'])
            # plt.subplot(3,1,2)
            # plt.plot(df['accumulate_change_ratio'])
            # plt.subplot(3,1,3)
            # plt.plot(df['smooth_accumulate_change_ratio'])
            # plt.show()
            df.index = range(df.shape[0])
            self.cache_data[s] = df
            self.last_am_count[s] = am.count
            self.highest_track[s] = am.close[-1]


        # self.log(str_log)
        self.trade_history = dict()

    def on_after_trading(self, date_time):
        """收盘时触发一次回调, 港股是16:00:00"""
        str_log = "on_after_trading - %s" % date_time.strftime('%Y-%m-%d %H:%M:%S')
        self.log(str_log)
        self.plot_result(date_time)

    def sma(self, np_array, n, array=False):
        """简单均线"""
        if n < 2:
            result = np_array
        else:
            result = talib.SMA(np_array, n)
        if array:
            return result
        return result[-1]

    def ema(self, np_array, n, array=False):
        """移动均线"""
        if n < 2:
            result = np_array
        else:
            result = talib.EMA(np_array, n)
        if array:
            return result
        return result[-1]

    def calc_index(self, tiny_bar):
        """计算策略指标"""
        bar = tiny_bar
        symbol = bar.symbol
        # 得到分k数据的ArrayManager(vnpy)对象
        am = self.get_kl_min1_am(symbol)
        am_close = am.close[am.size - am.count:]
        last_count = self.last_am_count[symbol]
        for i in range(last_count, am.count):
            last_cache = self.cache_data[symbol].iloc[-1]
            close = am_close[i]
            cr = (close - last_cache['close']) / last_cache['close'] * 100
            acc_ratio = accumulate_ratio_(cr, last_cache['accumulate_change_ratio'])
            udc = up_down_count_(cr, last_cache['up_down_count'])
            sar = smooth_accumulate_ratio_(cr, acc_ratio, udc, last_cache['smooth_accumulate_change_ratio'],
                                           SMOOTH_THRESH)

            this_am = pd.DataFrame([[close, cr, acc_ratio, udc, sar]], columns=COLUMNS, index=[i])

            self.cache_data[symbol] = self.cache_data[symbol].append(this_am)
            last_count = last_count + 1
            self.last_am_count[symbol] = last_count
            if close > self.highest_track[symbol]:
                self.highest_track[symbol] = close

    def buy_decide(self, tiny_bar, minute = 0):
        bar = tiny_bar
        symbol = bar.symbol

        params = self.params_pools[symbol]
        cache = self.cache_data[symbol]
        this_cache = cache.iloc[-1]
        last_cache = cache.iloc[-2]
        this_acc_ratio = this_cache['accumulate_change_ratio']
        last_acc_ratio = last_cache['accumulate_change_ratio']
        last_smooth_acc = last_cache['smooth_accumulate_change_ratio']
        last_udc = last_cache['up_down_count']
        drop_rate_thresh = 0.1
        avg_drop_rate = last_acc_ratio / last_udc
        if this_acc_ratio > 0 and avg_drop_rate > drop_rate_thresh and (last_acc_ratio < params['buy_thresh'] or last_smooth_acc < params['smooth_buy_thresh']):
            self.log("buy decide true, symbol:%s, price:%.2f, acc_ratio:%.3f,  last_acc_ratio:%.2f, drop_rate:%.2f" % (
            tiny_bar.symbol, tiny_bar.close, this_acc_ratio, last_acc_ratio, avg_drop_rate))
            return True
        else:
            return False

    def sell_decide(self, tiny_bar, symbol, minute):
        """固定阈值"""
        params = self.params_pools[symbol]
        change_to_max = (tiny_bar.close - self.highest_track[symbol]) / self.highest_track[symbol] * 100
        if change_to_max < params["sell_thresh"] or minute >= 959:  # 16:59分，收市前一分钟卖出
            return True
        else:
            return False

    def sell_decide2(self, tiny_bar, symbol, minute):
        """动态阈值，跌幅越大，阈值越大"""
        params = self.params_pools[symbol]
        change_to_max = (tiny_bar.close - self.highest_track[symbol]) / self.highest_track[symbol] * 100
        pos = self.position_list[symbol]
        cache = self.cache_data[symbol]
        buy_index = pos['index']
        last_cache = cache.iloc[buy_index - 1]
        last_smooth_acc = last_cache['smooth_accumulate_change_ratio']
        sell_thresh = last_smooth_acc / params['dyn_thresh_factor']
        # self.log("sell_decide2 thresh %.5f" % sell_thresh)
        if change_to_max < sell_thresh or minute >= 959:  # 16:59分，收市前一分钟卖出
            return True
        else:
            return False

    def buy_decide_warrant(self, tiny_bar, minute=0):
        if minute > 0 and minute < 600:
            """早上10：00前，只要上涨立马买入"""
            cache = self.cache_data[tiny_bar.symbol]
            this_cache = cache.iloc[-1]
            this_acc_ratio = this_cache['accumulate_change_ratio']
            if (this_acc_ratio > 0):
                self.log("buy decide true, symbol:%s, price:%.2f, acc_ratio:%.3f" %(tiny_bar.symbol, tiny_bar.close, this_acc_ratio))
                return True

        return self.buy_decide(tiny_bar)


    def sell_decide_warrant(self, tiny_bar, symbol, minute):
        """涡轮卖出信号，只要下跌立马卖出"""
        cache = self.cache_data[symbol]
        this_cache = cache.iloc[-1]
        this_acc_ratio = this_cache['accumulate_change_ratio']
        if this_acc_ratio < 0 or minute >= 959:  # 15:59分，收市前一分钟卖出
            return True
        else:
            return False

    def buy_stock(self, tiny_bar, call_or_put):
        bar = tiny_bar
        symbol = bar.symbol
        params = self.params_pools[symbol]
        if call_or_put == 'call':
            buy_target = params['war_call']
            buy_volume = params['call_vol']
        else:
            buy_target = params['war_put']
            buy_volume = params['put_vol']

        price = self.get_last_price(buy_target)
        price = price + 0.004
        self.buy(price, buy_volume, buy_target)  # 竞价单
        am = self.get_kl_min1_am(symbol)
        info = TradeInfo()
        info.symbol = buy_target
        info.warrant_stock = symbol
        info.price = price
        info.price_stock = bar.close
        info.volume = buy_volume
        info.index = am.count - 1
        info.datetime = bar.datetime
        self.buying_list[symbol] = info

    def sell_stock(self, tiny_bar, call_or_put):
        bar = tiny_bar
        symbol = bar.symbol
        pos_info = self.position_list[symbol]
        last_price = self.get_last_price(pos_info.price)
        last_price = last_price - 0.004
        self.sell(last_price, pos_info.volume, pos_info.symbol, datetime=tiny_bar.datetime)
        sell_info = pos_info
        self.selling_list[symbol] = sell_info
        self.position_list.pop(symbol)

    def buy_impl(self, tiny_bar):
        minute = tiny_bar.datetime.hour * 60 + tiny_bar.datetime.minute # 从凌晨00：00到现在的分钟数
        # 16:55分，收市前5分钟, 不要买入股票
        if minute > 955:
            return

        bar = tiny_bar
        symbol = bar.symbol
        params = self.params_pools[symbol]
        if self.buy_decide(tiny_bar):
            power = self.get_power()
            # volume = math.floor(power / bar.close / params['lot_size']) * params['lot_size']
            self.buy_stock(tiny_bar, 'call')
            cache = self.cache_data[symbol]
            last_cache = cache.iloc[-2]
            last_smooth_acc = last_cache['smooth_accumulate_change_ratio']
            sell_thresh = last_smooth_acc / params['dyn_thresh_factor']
            self.highest_track[symbol] = bar.close
            am = self.get_kl_min1_am(symbol)
            self.log("buy %s, price: %.2f, volume: %d, index: %d, sell_thresh:%.5f"
                         % (symbol, bar.close,  am.count - 1, sell_thresh))

    def sell_impl(self, tiny_bar):
        bar = tiny_bar
        symbol = bar.symbol

        if symbol not in self.position_list.keys():
            return

        pos = self.position_list[symbol]
        minute = tiny_bar.datetime.hour * 60 + tiny_bar.datetime.minute # 从凌晨00：00到现在的分钟数
        if pos is not None:
            if self.sell_decide_warrant(bar, symbol, minute):
                self.sell_stock(tiny_bar, "call")

                am = self.get_kl_min1_am(symbol)
                power = self.get_power()
                self.log("sell %s. index=%d, sell price: %.2f, buy_price: %.2f, power: %.2f"
                      % (symbol, am.count - 1, bar.close, pos.price_stock, power))
                history = TradeHistory()
                history.volume = pos.volume
                history.symbol = pos.symbol
                history.sell_price = bar.close
                history.buy_price = pos.price_stock
                history.sell_index = am.count - 1
                history.buy_index = pos['index']
                history.earn = history.sell_price - history.buy_price
                history.sell_datetime = tiny_bar.datetime
                history.buy_datetime = pos.datetime
                if symbol not in self.trade_history.keys():
                    self.trade_history[symbol]=[]
                self.trade_history[symbol].append(history)
                self.selling_list.pop(symbol) #假设一定能卖成功


    def check_position(self, tiny_bar):
        # 检测成交数量
        bar = tiny_bar
        symbol = bar.symbol
        if symbol not in self.buying_list.keys():
            return

        buying_info = self.buying_list[symbol]
        buying_volume = buying_info.volume
        pos = self.get_tiny_position(symbol)
        if pos is None:
            # TODO cancel order
            return

        pos_info = buying_info

        # 将下单价格和量修改为成交价格和量
        pos_info.price = pos.price
        pos_info.volume = pos.position

        if pos.position != buying_volume: #下单数量和成交数量不一样
            # TODO cancel order
            pass
        self.buying_list.pop(symbol)
        self.position_list[symbol] = pos_info

    def get_position_mask(self, trade_list, bar_count):
        mask = np.zeros(bar_count)
        for trade in trade_list:
            mask[trade.buy_index:trade.sell_index + 1] = 1
        return mask

    def get_profit(self, trade_list):
        profit = 0
        for trade in trade_list:
            profit += trade.earn
        return profit

    def plot_result(self, date_time):
        for symbol in self.symbol_pools:
            df = self.cache_data[symbol]
            count = df.shape[0]
            if symbol in self.trade_history.keys():
                trade = self.trade_history[symbol]
                position_mask = self.get_position_mask(trade, count)
                profit = self.get_profit(trade)
            else:
                position_mask = np.zeros(count)
                profit = 0

            start_index = 330
            plt.figure(figsize=(13, 9))
            ax = plt.subplot(3,1,1)
            plt.title("%s %s profit: %d" % (date_time.strftime('%Y-%m-%d'), symbol, profit))
            setAxis(ax, 100, 10)
            plt.plot(list(df['close'][start_index:]))
            maxi = max(df['close'][start_index:])
            plt.plot(position_mask[start_index:] * maxi)
            plt.ylim(min(df['close'][start_index:]), max(df['close'][start_index:]))
            plt.grid()
            ax = plt.subplot(3,1,2)
            setAxis(ax, 100, 10)
            plt.plot(list(df['accumulate_change_ratio'][start_index:]))
            maxi = max(df['accumulate_change_ratio'][start_index:])
            plt.plot(position_mask[start_index:] * maxi)
            plt.ylim(min(df['accumulate_change_ratio'][start_index:]), max(df['accumulate_change_ratio'][start_index:]))
            plt.grid()
            ax = plt.subplot(3, 1, 3)
            setAxis(ax, 100, 10)
            plt.plot(list(df['smooth_accumulate_change_ratio'][start_index:]))
            maxi = max(df['smooth_accumulate_change_ratio'])
            plt.ylim(min(df['smooth_accumulate_change_ratio'][start_index:]), max(df['smooth_accumulate_change_ratio'][start_index:]))
            plt.plot(position_mask[start_index:] * maxi)
            plt.grid()
            plt.show()