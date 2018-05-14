import pandas as pd
import time
start = time.clock()
store = pd.HDFStore('ticker_26.h5', 'r')
data = store.select("data")
# data = store.select("data", where=('price > 4'))
end = time.clock()
delta = end - start
print("time: ", delta)



