import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import talib
import scipy.stats as stats


def get_datetime(df):
    date = df['data_date']
    time = df['data_time']
    dt = datetime.datetime.strptime(time + " " + date, "%H:%M:%S %Y-%m-%d")
    return dt

def kdj(data, fk, sk, sd):
    pre_addition_num = fk + max(sk, sd)
    delta = data.index[1] - data.index[0]
    pre_addition_index = data.index[:pre_addition_num]
    pre_addition_index = pre_addition_index - delta * pre_addition_num
    pre_addition = pd.DataFrame({'open': data['open'][0], 'high': data['high'][0], 'low': data['low'][0], 'close': data['close'][0]}, index=pre_addition_index)
    data_extend = pre_addition.append(data)
    k, d = talib.STOCH(data_extend['high'], data_extend['low'], data_extend['close'], fastk_period=fk, slowk_period=sk,
                       slowk_matype=1, slowd_period=sd, slowd_matype=1)
    j = 3*k - 2*d
    return k[pre_addition_num:], d[pre_addition_num:], j[pre_addition_num:]



def get_short_signal(signal):
    #find first short index
    first_short_index = 0
    short_signal = signal.copy()
    while short_signal[first_short_index] != -1:
        first_short_index = first_short_index + 1
    short_signal[:first_short_index] = 0
    #-1开空仓，1平仓，如果-1和1不配对，即sum不等于0，最后一个数平仓
    if short_signal.sum() != 0:  #sum 不等于0，
        if short_signal[-1] == -1:
            short_signal[-1] = 0
        else:
            short_signal[-1] = 1

    return short_signal


def get_long_signal(signal):
    # find first short index
    first_long_index = 0
    long_signal = signal.copy()
    while signal[first_long_index] != 1:
        first_long_index = first_long_index + 1
    long_signal[:first_long_index] = 0
    # 1开多仓，-1平仓，如果-1和1不配对，即sum不等于0，最后一个数平仓
    if long_signal.sum() != 0:  # sum 不等于0，
        if long_signal[-1] == 1:
            long_signal[-1] = 0
        else:
            long_signal[-1] = -1
    return long_signal


def pre_process_data(df, resample_period):
    index = df.apply(get_datetime, axis=1)
    df.index = index
    start_time = datetime.datetime.strptime("9:30:00" + " " + df['data_date'][0], "%H:%M:%S %Y-%m-%d")
    df = df.loc[start_time:]
    last_price = df['last_price']
    df_resample = last_price.resample(resample_period, label='right', closed='right').ohlc()
    df_resample = df_resample.dropna()
    return df_resample


def get_signal_price(prices, signal):
    signal_prices = -prices * signal
    selector = ((signal == 1) | (signal == -1))
    return signal_prices[signal_prices.index[selector]]


def get_return(signal_price):
    open_price = signal_price.iloc[0::2]
    close_price = signal_price.iloc[1::2]
    return_values = open_price.values + close_price.values
    return pd.Series(return_values, close_price.index)


def gen_test_params(period_v, n1, n2):
    params = []
    for p in period_v:
        k_p = np.arange((int)(p / 4), (int)(3 * p / 4), n1)
        # d_p = np.arange(n2, p, n2)
        # print(p)
        # print(k_p)
        # print(d_p)
        for n in k_p:
            params += [(p, n, n)]
    return params


def analyze_returns(net_returns):
    """
    Perform a t-test, with the null hypothesis being that the mean return is zero.

    Parameters
    ----------
    net_returns : Pandas Series
        A Pandas Series for each date

    Returns
    -------
    t_value
        t-statistic from t-test
    p_value
        Corresponding p-value
    """
    # TODO: Perform one-tailed t-test on net_returns
    # Hint: You can use stats.ttest_1samp() to perform the test.
    #       However, this performs a two-tailed t-test.
    #       You'll need to divde the p-value by 2 to get the results of a one-tailed p-value.
    null_hypothesis = 0.0
    t, p = stats.ttest_1samp(net_returns, null_hypothesis)
    return t, p/2

def calc_return_with_params(param):
    dates = pd.date_range("2018/10/8", "2018/10/12")
    returns = pd.Series()
    n = 400
    for date in dates:
        path = "/Users/lingkunkong/histData/Quote_{}.h5".format(date.strftime("%Y-%m-%d"))
        f = pd.read_hdf(path)
        quote_data = pre_process_data(f, '6S')
        k, d, j = kdj(quote_data, param[0], param[1], param[2])
        """
        gen signal
        """
        signal = k[:n].fillna(method='bfill') > d[:n].fillna(method='bfill')
        signal = signal.astype(np.int)
        signal = signal - signal.shift(1)
        # print(signal)

        short_signal = get_short_signal(signal[:n])
        long_signal = get_long_signal(signal[:n])

        """
        gen log_return
        """
        log_price = np.log(quote_data['close'][:n])

        short_log_price = get_signal_price(log_price, short_signal)
        long_log_price = get_signal_price(log_price, long_signal)

        # print(short_log_price)
        # print(long_log_price)

        short_log_return = get_return(short_log_price)
        long_log_return = get_return(long_log_price)
        # print(short_log_return)
        # print(long_log_return)

        # log_return = pd.DataFrame(
        #     {'close': quote_data['close'][:n], 'long': long_log_return, "short": short_log_return})
        # # log_return.to_csv("/Users/lingkunkong/Documents/log_return_{}.csv".format(date.strftime("%Y-%m-%d")))
        # print(log_return)
        # print(" -------{}------".format(date))
        # print("short return {0} long return {1}, total return {2}".format(short_log_return.sum(), long_log_return.sum(),
        #                                                                   short_log_return.sum() + long_log_return.sum()))
        short_return = np.exp(short_log_return.sum())
        long_return = np.exp(long_log_return.sum())
        total_return = np.exp(short_log_return.sum() + long_log_return.sum())
        returns = returns.append(short_log_return)
        returns = returns.append(long_log_return)
        print("short return precent {:.3f}%, long return precent {:.3f}%, total {:.3f}".format((short_return - 1) * 100,
                                                                                               (long_return - 1) * 100,
                                                                                               (
                                                                                                           total_return - 1) * 100))
        # print("end time {}".format(log_price.index[-1]))

    returns = (np.exp(returns) - 1) * 100
    # print(returns)
    t, p = analyze_returns(returns)
    # print("t-statistic: {:.3f}\np-value: {:.6f}".format(t, p))
    return returns.sum(), p


if __name__ == '__main__':
    params = gen_test_params(np.arange(12, 30, 1), 1, 1)
    print(params)
    results = []
    params_count = len(params)
    i = 0
    for param in params:
        i = i + 1
        result = calc_return_with_params(param)
        results += [result]
        print("processing {}/{}, param {}".format(i, params_count, param))
        print(result)
    results_series = pd.Series(results, params)
    print(results_series)
    results_series.to_csv("/Users/lingkunkong/Documents/result_6s_2.csv")
    # calc_return_with_params((9, 6, 6))