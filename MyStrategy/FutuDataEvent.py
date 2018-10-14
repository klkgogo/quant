# encoding: UTF-8
'''

'''

import time
from copy import copy
from datetime import datetime, timedelta
# from .TinyDefine import *
# from .vnpyInc import *
import futuquant as ft


class FutuDataEvent(object):
    name = "FutuDataEvent"

    def __init__(self, quant_frame, quote_context, symbol_pools, subtype_list):
        self._quant_frame = quant_frame
        self._quote_context = quote_context
        self._symbol_pools = symbol_pools
        self._tick_dict = {}
        self._market_opened= False
        self.subscribe(symbol_pools, subtype_list)
        # # 控制频率，1秒钟最多推送quote多少次
        # self._push_event_freq = 10
        # self._dict_last_push_time = {}
        #
        # # 记录当前股票池的实时行情数据
        # self._rt_tiny_quote = {}
        #
        # self._sym_kline_am_dict = {}   # am = ArrayManager
        #
        # self._sym_kline_last_am_bar_dic = {} # 记录am 最后一个bar的数据
        # self._sym_kline_last_event_bar_dic = {} # 记录最后一个事件推送的bar
        # self._sym_kline_next_event_bar_dic = {} # 记录下一个准备推送的bar

        # # 注册事件
        # self._event_engine.register(EVENT_TINY_TICK, self._event_tiny_tick)
        # self._event_engine.register(EVENT_CUR_KLINE_PUSH, self._event_cur_kline_push)
        # self._event_engine.register(EVENT_BEFORE_TRADING, self.__event_before_trading)
        # self._event_engine.register(EVENT_AFTER_TRADING, self.__event_after_trading)
        # self._event_engine.register(EVENT_AFTER_TRADING_FINAL, self.__event_after_trading_final)

        class QuoteHandler(ft.StockQuoteHandlerBase):
            """报价处理器"""
            futu_data_event = self

            def on_recv_rsp(self, rsp_str):
                ret_code, content = super(QuoteHandler, self).on_recv_rsp(rsp_str)
                if ret_code != ft.RET_OK:
                    return ft.RET_ERROR, content
                self.futu_data_event.process_quote(content)
                return ft.RET_OK, content

        class OrderBookHandler(ft.OrderBookHandlerBase):
            """摆盘处理器"""
            futu_data_event = self

            def on_recv_rsp(self, rsp_str):
                ret_code, content = super(OrderBookHandler, self).on_recv_rsp(rsp_str)
                if ret_code != ft.RET_OK:
                    return ft.RET_ERROR, content
                self.futu_data_event.process_orderbook(content)
                return ft.RET_OK, content

        class CurKlineHandler(ft.CurKlineHandlerBase):
            """实时k线推送处理器"""
            futu_data_event = self

            def on_recv_rsp(self, rsp_str):
                ret_code, content = super(CurKlineHandler, self).on_recv_rsp(rsp_str)
                if ret_code != ft.RET_OK:
                    return ft.RET_ERROR, content
                self.futu_data_event.process_curkline(content)
                return ft.RET_OK, content

        # 设置回调处理对象
        self._quote_context.set_handler(QuoteHandler())
        self._quote_context.set_handler(OrderBookHandler())
        self._quote_context.set_handler(CurKlineHandler())

        # # 定阅数据
        # subtype_list = [ft.SubType.QUOTE, ft.SubType.ORDER_BOOK, ft.SubType.K_DAY, ft.SubType.K_1M]
        # ret, data = self._quote_context.subscribe(symbol_pools, subtype_list)
        # if ret != ft.RET_OK:
        #     raise Exception('订阅行情失败：{}'.format(data))

    def stop(self):
        self._quote_context.close()

    def subscribe(self, symbol_pools, subtype_list):
        ret, data = self._quote_context.subscribe(symbol_pools, subtype_list)
        if ret != ft.RET_OK:
            raise Exception('订阅行情失败：{}'.format(data))

    def process_quote(self, data):
        """报价推送"""
        #todo
        self._quant_frame.on_quote_change(data)

    def process_orderbook(self, data):
        """订单簿推送"""
        #todo
        pass

    def process_curkline(self, data):
        #todo
        pass