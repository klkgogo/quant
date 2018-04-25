import numpy as np
import math

def change_ratio(data):
    d = np.diff(data)
    print("diff ", d)
    ratio = [d[i] / data[i] * 100 for i in range(len(d))]
    return ratio


def accumulate_ratio_(cur, last):
    #cur和last的符号相等，反回两个的相加，若不相等返回cur
    if cur * last > 0:
        return cur + last
    else:
        return cur

def accumulate_ratio(data):
    last = 0
    ret = np.zeros(len(data))
    for i in range(len(data)):
        ret[i] = accumulate_ratio_(data[i], last)
        last = ret[i]
    return ret

def smooth_accumulate_ratio_(cur_ratio, cur_acc_ratio, cur_up_down_count, last_smooth, thresh):
    if not last_smooth == 0 and math.fabs(cur_acc_ratio / last_smooth) < thresh:
        #上涨和下跌过程回调幅度小于thresh认为是过程中的小毛刺，不改变上涨和下跌趋势
        return last_smooth + cur_ratio
    else:
        if last_smooth * cur_ratio > 0:
            return last_smooth + cur_ratio
        else:
            return cur_acc_ratio


def smooth_accumulate_ratio(ratio, acc_ratio, up_down_count, thresh):
    #过虑下跌或上涨过程中的一些小回调，
    ret = np.zeros(len(ratio))
    last_smooth = 0
    last_acc_ratio = 0
    for i in range(len(ratio)):
        ret[i] = smooth_accumulate_ratio_(ratio[i], acc_ratio[i], up_down_count[i], last_smooth, thresh)
        last_smooth = ret[i]
    return ret

def up_down_count_(cur, last):
    if cur * last > 0:
        if cur > 0:
            return last + 1
        else:
            return last - 1
    else:
        if cur > 0:
            return 1
        else:
            return -1


def up_down_count(data):
    #连续上涨和下跌的次数1为上涨1次，-1为下跌一次
    last = 0
    ret = np.zeros(len(data))
    for i in range(len(data)):
        ret[i] = up_down_count_(data[i], last)
        last = ret[i]
    return ret

def test_change_ratio():
    list = np.random.rand(10)
    list = list + 100
    print(list)
    print(change_ratio(list))

def test_sum_ratio():
    list = np.array([100.1, 100.5, 100.7, 101, 101.2, 101, 101.5, 101.1, 101, 100.5, 100, 100.1, 100, 99.8])
    list = list
    ratio = change_ratio(list)
    ar = accumulate_ratio(ratio)
    udc = up_down_count(ratio)
    sar = smooth_accumulate_ratio(ratio, ar, udc, 0.3)
    print("ratio")
    print(ratio)
    print("ar")
    print(ar)
    print("udc")
    print(udc)
    print("sar")
    print(sar)

if __name__ == '__main__':
    # test_change_ratio()
    test_sum_ratio()