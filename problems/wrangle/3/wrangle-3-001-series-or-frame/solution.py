import pandas as pd
t = pd.DataFrame({"stock": [4, 1, 6]})
print(t["stock"].shape)
print(t[["stock"]].shape)
