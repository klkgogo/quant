import pandas as pd
import time
start = time.clock()
store = pd.HDFStore('ticker_26.h5', 'r')
#data = store.select("data", where=('code=="HK.00700"'))
data = store.select("data", where=('price > 4'))
print(data)
end = time.clock()
delta = end - start
print("time: ", delta)

