import pandas as pd
a = pd.DataFrame({"id": [2, 3]})
b = pd.DataFrame({"id": [2, 2, 2, 3]})
print(len(a.merge(b, on="id", how="inner")))
