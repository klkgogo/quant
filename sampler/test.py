import pandas as pd
import datetime as dt
df = pd.DataFrame([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]], columns=['a', 'b', 'c', 'd', 'e'])
df['f'] = 10
print(df)
print(df[['a', 'e']])
print(dt.datetime.now())