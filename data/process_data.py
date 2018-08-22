import pandas as pd
import numpy as np
import time
import datetime as dt

PROCESSED_PATH = "../data/processed"
RAW_PATH = "../data/raw"

def process_ticker(timestamp):
    date = "%d-%02d-%02d" % (timestamp.year, timestamp.month, timestamp.day)
    try:
        file_name = '%s/ticker_%s.h5' % (RAW_PATH, date)
        src = pd.HDFStore(file_name, 'r')
    except (IOError) as e:
        print("error file %s not exist" % file_name)
        return

    data = src['data']

    print("process %s" % file_name)
    code_set = set(data['code'])
    for code in code_set:
        print('%s add %s' % (date, code))
        ret = read_ticker(code, pd.Period(date))
        if (ret is not None) and not ret.empty:
            print("%s %s already exist!" % (date, code))
            continue

        ticker = data[data['code'] == code]
        time = ticker['time'].values
        index = [pd.Timestamp(t) for t in time]
        ticker.index = index
        dst_file_name = '%s/%s.h5' % (PROCESSED_PATH, code)
        dst = pd.HDFStore(dst_file_name, 'a')
        dst.append('ticker', ticker)
        dst.close()

    src.close()

def process_orderbook(timestamp):
    date = "%d-%02d-%02d" % (timestamp.year, timestamp.month, timestamp.day)
    try:
        file_name = '%s/orderbook_%s.h5' % (RAW_PATH, date)
        src = pd.HDFStore(file_name, 'r')
    except (IOError) as e:
        print("error file %s not exist" % file_name)
        return

    data = src['data']
    data.rename(columns = {'stcok_code':'code', 'timestamp':'time'}, inplace=True)
    print(data.info())
    code_set = set(data['code'])
    print("process %s" % file_name)
    for code in code_set:
        print('orederbook %s add %s' % (date, code))
        # ret = read_orderbook(code, pd.Period(date))
        # if (ret is not None) and not ret.empty:
        #     print("%s %s already exist!" % (date, code))
        #     continue

        od = data[data['code'] == code]
        time = od['time'].values
        index = [pd.Timestamp(t) for t in time]
        od.index = index
        dst_file_name = '%s/%s.h5' % (PROCESSED_PATH, code)
        dst = pd.HDFStore(dst_file_name, 'a')
        dst.append('orderbook', od)
        dst.close()

    src.close()


def read_orderbook(code, period):
    try:
        file_name = '%s/%s.h5' % (PROCESSED_PATH, code)
        st = pd.HDFStore(file_name, 'r')
    except (IOError) as e:
        return None

    data = st.select('orderbook', 'index >= period.start_time & index < period.end_time')
    st.close()
    return data

def read_ticker(code, period):
    """

    :param code: 股票代码
    :param period: pd.Period()对像，例pd.Period('2018-4-17')
    :return:
    """
    try:
        file_name = '%s/%s.h5' % (PROCESSED_PATH, code)
        st = pd.HDFStore(file_name, 'r')
    except (IOError) as e:
        return None

    data = st.select('ticker', 'index >= period.start_time & index < period.end_time')
    data[['volume', 'turnover']] = data[['volume', 'turnover']].astype(float)
    st.close()
    return data

def change_tickre_to_candle(ticker, timestamp):
    code = ticker['code'][0]
    time_key = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    open = ticker['price'][0]
    close = ticker['price'][-1]
    low = ticker['price'].min()
    high = ticker['price'].max()
    volume = ticker['volume'].sum()
    turnover = ticker['turnover'].sum()
    data = {'code':[code], 'time_key':[time_key], 'open':[open], 'close':[close], 'low':[low],'high':[high], 'volume':[volume], 'turnover':[turnover]}
    df = pd.DataFrame(data=data, index=[timestamp])
    return df



def construct_kline_from_ticker(ticker, delta):
    """
    从ticker数据合成kline
    :param ticker:  ticker数据
    :param period:  kline周期，以秒为单位。
    :return: kline格式和 get_cur_kline一样
    """
    ticker.sort_index(inplace=True)
    rows_count = ticker.shape[0];
    start_time = pd.Timestamp(ticker.index[0]);
    end_time = pd.Timestamp(ticker.index[rows_count - 1])
    delta_time = pd.Timedelta(seconds=delta)
    last_close = ticker['price'][0]
    code = ticker['code'][0]

    slice_timeidx = pd.DatetimeIndex(start=start_time, end=end_time, freq='{0}S'.format(delta))
    # 上一条语句生成的时间序列，不大于end_time，所以为了能包括end_time,再添加一个时间点。
    slice_timeidx = slice_timeidx.append(pd.DatetimeIndex([slice_timeidx[-1] + delta_time]))

    # 得到时间点对应的idx, 使用idx切片索引要比直接用DatetimeIndex切片快大约20%
    start_slice_idx = np.searchsorted(ticker.index, slice_timeidx)
    start_idx = start_slice_idx[0]
    iter_start_idx = start_slice_idx[1:]

    # 使用np array存放数据比df.append快8倍
    data_array = np.zeros((len(iter_start_idx), 6))
    i = 0
    for idx in iter(iter_start_idx):
        # end = start + delta_time
        end_idx = idx
        data = ticker[start_idx:end_idx] #前闭后开
        if data.empty:
            item = np.array([last_close, last_close, last_close, last_close, 0, 0])
            data_array[i, :] = item
        else:
            price = data['price'].values
            open = price[0]
            close = price[-1]
            low = price.min()
            high = price.max()
            volume = data['volume'].sum()
            turnover = data['turnover'].sum()
            item = np.array([open, close, low, high, volume, turnover])
            data_array[i, :] = item
            last_close = close
        start_idx = idx
        i = i + 1

    df = pd.DataFrame(data=data_array, index=slice_timeidx[1:], columns=['open', 'close', 'low', 'high', 'volume', 'turnover'])
    df['time_key'] = slice_timeidx[1:]
    df['code'] = code
    return df


def process():
    date = pd.date_range('2018-04-27', '2018-05-30')
    for d in date:
        process_ticker(d)
        process_orderbook(d)


def test_read():

    data = read_ticker('HK.00700', pd.Period('2018-4-27'))

    start = time.clock()
    df = construct_kline_from_ticker(data, 30)
    end = time.clock()
    print(df)
    print('time %f' % (end - start))



if __name__ == '__main__':
    a = np.array([[1,2,3], [4,5,6]])
    df = pd.DataFrame(data=a, columns=list('abc'))
    print(df)
    # a = n.hstack([4])
    # print(a)
    test_read()
    # a = [1:1:5]


