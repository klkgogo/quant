import pandas as pd
import time
start = time.clock()
store = pd.HDFStore('../data/ticker_2018-04-26.h5', 'r')
store.create_table_index('data', columns=['code'], optlevel=9, kind='full')

st = pd.HDFStore('test.h5', 'w')
# data = store.select("data")
data = store.select("data")
print(store.get_storer('data'))
hk00700 = data[data['code'] == 'HK.00700']
end = time.clock()
delta = end - start
t = hk00700['time'].values
i = [pd.Timestamp(tt) for tt in t]
# print(i)
hk00700.index = i
print(hk00700)

# t = hk00700['time']
print(hk00700.info())
print(type(hk00700.index))
# st['HK.00700'] = hk00700
st.append("ticker", hk00700)
# print(data)
print("time: ", delta)
print(st.get_storer('ticker'))
store.close()
st.close()

st = pd.HDFStore('test.h5', 'r')
data = st.select('ticker', )
# data = st['ticker']['2018-4-27']
print(data['2018-04-27 9:30:00' : '2018-04-27 9:30:02'])
st.close()



