import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

d = np.arange(0, 10)
d2 = np.arange(1, 11)
df = DataFrame(d)
df2 = DataFrame(d2)
print(df)
df = df.append(df2)
print(df)
print(df.shape)

df = DataFrame()
print(df)

