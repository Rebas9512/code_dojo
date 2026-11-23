import pandas as pd
s = pd.Series([3, -4, -1])
print(s.apply(abs).tolist())
