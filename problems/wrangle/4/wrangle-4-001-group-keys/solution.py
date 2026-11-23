import pandas as pd
t = pd.DataFrame({"rack": ["A", "A", "B"], "n": [2, 1, 0]})
s = t.groupby("rack").agg(total=("n", "sum"))
print(s.columns.tolist())
print(s.reset_index().columns.tolist())
