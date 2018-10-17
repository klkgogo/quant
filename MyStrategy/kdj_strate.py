from MyStrategy.FutuQuantFrame import *
from MyStrategy.StrateBase import *
import futuquant as ft
import time
import pandas as pd
import datetime
import talib
import math



def kdj(data, fk, sk, sd):
    k, d = talib.STOCH(data['high'], data['low'], data['close'], fastk_period=fk, slowk_period=sk,
                       slowk_matype=1, slowd_period=sd, slowd_matype=1)
    return k, d

class KDJStrate(StrateBase):

    subtype_list = [ft.SubType.QUOTE]
    sample_frequent = 15 #每二秒推送一次报价，3次为6s
    fk = 60
    sk = 20
    sd = 20

    power = 5000

    short_code = 'HK.66491'
    long_code = 'HK.66518'
    symbol_pools = ['HK.800000', short_code, long_code]

    def __init__(self):
        super(KDJStrate, self).__init__()
        self.cache = pd.DataFrame()
        self.sample_records = pd.DataFrame()
        self.date = datetime.datetime.now().date()
        self.market_snapshot = 0
        self.last_append_time = ""

    def on_init_strate(self):
        self.logger.info("on_init_strate")
        self.market_snapshot = self._quant_frame.get_snapshot([self.short_code, self.long_code])
        self.market_snapshot.index = self.market_snapshot['code']

    def on_strate_close(self):
        self.logger.info("on_strate_close")

    def gen_resample_record(self, data):
        open = data['open_price'].iloc[0]
        high = data['high_price'].max()
        low = data['low_price'].min()
        close = data['last_price'].iloc[-1]
        date_time = datetime.datetime.strptime(data['data_time'].iloc[-1] + " " + data['data_date'].iloc[-1], "%H:%M:%S %Y-%m-%d")
        record = pd.DataFrame({'open': open, 'high': high, 'low': low, 'close': close}, index=[date_time])
        return record


    def on_quote_changed(self, data):
        # self.logger.info("on_quote_changed: {}".format(data))
        for ix, row in data.iterrows():
            if row['code'] != 'HK.800000':
                continue
            # self.logger.info("last:{}, current:{}, same:{}".format(self.last_append_time, row['data_time'], self.last_append_time == row['data_time']));
            #恒生指数会推送两次，一次推送报价，第二次推送成交量
            if self.last_append_time == row['data_time']:
                continue

            self.cache = self.cache.append(row)
            self.logger.info(
                "on quote_changed {}: last: {}, open:{}, high:{}, low: {}, count:{}".format(
                    row['data_time'], row['last_price'], row['open_price'], row['high_price'], row['low_price'], self.cache.shape[0]))
            self.last_append_time = row['data_time']

            if self.cache.shape[0] == self.sample_frequent:
                record = self.gen_resample_record(self.cache)
                self.logger.info(
                    "new record\n {}".format(record))
                self.sample_records = self.sample_records.append(record)
                if self.sample_records.shape[0] == 1: #避免计算kdj出现NaN, 向前扩展sample_records
                    self.extend_sample_records()
                if self.sample_records.shape[0] > 5:
                    self.run_strate()
                self.cache = pd.DataFrame()


    def extend_sample_records(self):
        pre_addition_num = self.fk + max(self.sk, self.sd)
        delta = datetime.timedelta(seconds= self.sample_frequent * 2)
        pre_end = datetime.datetime.strptime(self.date.strftime("%Y-%m-%d") + " 09:30:00",  "%Y-%m-%d %H:%M:%S")
        pre_start = pre_end - delta * pre_addition_num
        pre_addition_range = pd.date_range(pre_start, pre_end, freq='6S')
        print(pre_addition_range)
        pre_addition = pd.DataFrame(
            {'open': self.sample_records['open'].iloc[0], 'high': self.sample_records['high'].iloc[0], 'low': self.sample_records['low'].iloc[0], 'close': self.sample_records['close'].iloc[0]},
            index=pre_addition_range)
        self.sample_records = self.sample_records.append(pre_addition)


    def run_strate(self):
        k, d = kdj(self.sample_records, self.fk, self.sk, self.sd)
        # k线下穿d线，开空仓，平多仓
        self.logger.info("run_strate, lastk: {}, lastd: {}, thisK: {}, thisD: {}".format(k[-2], d[-2], k[-1], d[-1]))
        if k[-2] >= d[-2] and k[-1] < d[-1]:
            self.logger.info("keep short")
            self.open_position(self.short_code)
            self.close_position(self.long_code)

        # k线上穿d线，平空仓，
        # 开多仓
        if k[-2] <= d[-2] and k[-1] > d[-1]:
            self.logger.info("keep long")
            self.close_position(self.short_code)
            self.open_position(self.long_code)

    def get_open_order_params(self, quote):
        self.logger.info("get_open_order_params {}".format(quote))
        order_price = quote['last_price'].iloc[0] + quote['price_spread'].iloc[0] * 2
        lot_size = self.market_snapshot['lot_size'].loc[quote['code'].loc[0]]
        self.logger.info("lot_size {}, price {}".format(lot_size, order_price))
        lot_price = lot_size * order_price
        lot_num = math.floor(self.power / lot_price)
        order_vol = lot_size * lot_num
        return order_price, order_vol

    def get_close_order_params(self, quote):
        order_price = quote['last_price'].iloc[0] - quote['price_spread'].iloc[0] * 2
        pos = self._quant_frame.get_tiny_position(quote['code'].loc[0])
        return order_price, pos

    def open_position(self, code):
        quote = self._quant_frame.get_rt_quote(code)
        order_price, order_vol = self.get_open_order_params(quote)
        ret, data = self.buy(order_price, order_vol, code)
        self.logger.warn("buy: {} at: {} , last_price:{} vol: {}, ret: {}, info: {}".format(code, order_price, quote['last_price'].iloc[0], order_vol, ret, data))

    def close_position(self, code):
        quote = self._quant_frame.get_rt_quote(code)
        order_price, pos = self.get_close_order_params(quote)
        if not pos:
            self.logger.warn("no position to close {}".format(code))
        else:
            ret, data = self.sell(order_price, pos.position, code)
            self.logger.warn("sell: {} at: {}, cost_price: {}, last_price:{} vol: {}, ret: {}, info: {}".format(code, order_price, pos.price,  quote['last_price'].iloc[0], pos.position, ret, data))

if __name__ == '__main__':
    frame = FutuQuantFrame('127.0.0.1', 11111, MARKET_HK)
    strate = KDJStrate()
    strate.init_strate(frame)
    while True:
        time.sleep(10)
    strate.close()
    # df = pd.DataFrame({"open":[1,2,3]}, index=[0,1,2])
    # print(df['open'].iloc[-1])

