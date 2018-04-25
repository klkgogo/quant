import ast
import pandas as pd
import numpy as np
import datetime as dt

orderbook = "{'stock_code': 'US.GOOG', 'Ask': [(1034.92, 100, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0)], 'Bid': [(1033.81, 200, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0), (0.0, 0, 0)], 'timestamp': 1522336319.994603}"

d = ast.literal_eval(orderbook)
print(d)

print(list(d.keys()))
print(list(d.values()))

df = pd.DataFrame(d)

print(df)


# f = pd.HDFStore("data/test.h5", 'w')
# f['data'] = df
# f.close()

tp = (1, 2, 3)
print(range(10))
indexAsk = ['Ask_price' + str(x) for x in range(10)]
indexAsk_volume = ['Ask_volume' + str(x) for x in range(10)]
indexAsk_num = ['Ask_num' + str(x) for x in range(10)]

valuesAsk = [x[0] for x in d['Ask']]
valuesAskV = [x[1] for x in d['Ask']]
valuesAskN = [x[2] for x in d['Ask']]

print(indexAsk)
indexBid = ['Bid_price' + str(x) for x in range(10)][::-1]
indexBid_volume = ['Bid_volume' + str(x) for x in range(10)][::-1]
indexBid_num = ['Bid_num' + str(x) for x in range(10)][::-1]

valuesBid = [x[0] for x in d['Bid']][::-1]
valuesBidV = [x[1] for x in d['Bid']][::-1]
valuesBidN = [x[2] for x in d['Bid']][::-1]

print(indexBid)
print(list(x[0] for x in df['Ask']))

def genColums():
    indexAsk = ['Ask_price' + str(x) for x in range(10)]
    indexAsk_volume = ['Ask_volume' + str(x) for x in range(10)]
    indexAsk_num = ['Ask_num' + str(x) for x in range(10)]

    indexBid = ['Bid_price' + str(x) for x in range(10)][::-1]
    indexBid_volume = ['Bid_volume' + str(x) for x in range(10)][::-1]
    indexBid_num = ['Bid_num' + str(x) for x in range(10)][::-1]
    index = indexBid + indexAsk + indexBid_volume + indexAsk_volume + indexBid_num + indexAsk_num + ['stcok_code', 'timestamp']
    return index

def changeOrderBookValueToList(ob):
    valuesAsk = [x[0] for x in ob['Ask']]
    valuesAskV = [x[1] for x in ob['Ask']]
    valuesAskN = [x[2] for x in ob['Ask']]

    valuesBid = [x[0] for x in ob['Bid']][::-1]
    valuesBidV = [x[1] for x in ob['Bid']][::-1]
    valuesBidN = [x[2] for x in ob['Bid']][::-1]
    values = valuesBid + valuesAsk + valuesBidV + valuesAskV + valuesBidN + valuesAskN + [d['stock_code'] , dt.datetime.now()]
    return values
df = pd.DataFrame([changeOrderBookValueToList(d)], columns=genColums())
print(df)

print(str(dt.datetime.now())[:10])