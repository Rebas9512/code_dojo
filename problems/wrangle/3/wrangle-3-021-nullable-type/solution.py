import pandas as pd
s = pd.Series([7, None, 0])
print(s.dtype)
print(s.astype("Int64").dtype)
