import pandas as pd

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
    st.close()
    return data

def process():
    date = pd.date_range('2018-04-27', '2018-05-30')
    for d in date:
        process_ticker(d)

def test_read():
    data = read_ticker('HK.00700', pd.Period('2018-4-27'))
    print(data)

if __name__ == '__main__':
    # test_read()
    process()


