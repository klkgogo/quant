import pandas as pd

f = pd.read_hdf("/Users/lingkunkong/Downloads/Quote_2018-10-09.h5")
print(f[:600])
# st = pd.HDFStore("/Users/lingkunkong/Downloads/Quote_2018-10-08.h5", 'r')
# print(st['data'])
# st.close()
#
# f = pd.read_hdf("/Users/lingkunkong/Downloads/ticker_2018-10-08.h5")
# print(f)
# print(f[f['code'] == 'HK.63257'])
#
# f = pd.read_hdf("Quote_2018-10-08.h5")
# print(f)
