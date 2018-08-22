# -*- coding: utf-8 -*-
"""
验证接口：获取某个市场的全部快照数据
"""
import time
import pandas as pd
import futuquant as ft
import datetime as dt
from sqlalchemy import create_engine


def loop_get_mkt_snapshot(context, market):
    """
    验证接口：获取某个市场的全部快照数据 get_mkt_snapshot
    :param api_svr_ip: (string)ip
    :param api_svr_port: (int)port
    :param market: market type
    :return:
    """
    # 创建行情api
    ret_code, basicinfo = context.get_stock_basicinfo(market, ft.SecurityType.STOCK)

    stock_codes = basicinfo['code'].values
    if len(stock_codes) == 0:
        quote_ctx.close()
        print("Error market:'{}' can not get stock info".format(market))
        return

    # 按频率限制获取股票快照: 每5秒200支股票
    snapshot = pd.DataFrame()
    print(len(stock_codes))
    for i in range(0, len(stock_codes), 200):
        print("from {}, total {}".format(i, len(stock_codes)))
        ret_code, ret_data = context.get_market_snapshot(list(stock_codes[i:i + 200]))
        if ret_code != 0:
            print(ret_data)
        else:
            snapshot = snapshot.append(ret_data)
        time.sleep(6)
        # break
    info = pd.merge(basicinfo, snapshot, on=['code', 'listing_date', 'lot_size'])
    return info

if __name__ == "__main__":
    # ip = 'lim.app'
    # port = 11113
    ip = "192.168.56.2"
    port = 11111
    db_info = {'user': 'root',
               'password': 'abc123456',
               'host': 'localhost',
               'database': 'xx_db'
               }

    engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s/%(database)s?charset=utf8' % db_info,
                           encoding='utf-8')

    dt_now = dt.datetime.now()
    now = dt_now.strftime("%Y-%m-%d")

    quote_ctx = ft.OpenQuoteContext(host=ip, port=port)
    for mkt in [ft.Market.SZ]:
        info = loop_get_mkt_snapshot(quote_ctx, mkt)
        info.to_sql("{}_{}".format(now, mkt), engine, if_exists='replace')

    quote_ctx.close()