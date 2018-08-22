import pandas as pd

df = pd.DataFrame([[1,2,3], [4,5,6]], columns=list('abc'))
df['d'] = [5,6]
print(df)