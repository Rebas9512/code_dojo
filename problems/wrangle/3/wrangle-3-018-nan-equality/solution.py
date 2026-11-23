import pandas as pd
s = pd.Series([2.0, float("nan")])
x = s.iloc[1]
print(x == x)
print(s.isna().tolist())
