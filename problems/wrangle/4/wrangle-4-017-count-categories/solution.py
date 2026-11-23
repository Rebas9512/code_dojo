import pandas as pd
s = pd.Series(["A", None, "A", "B"])
print(len(s.value_counts()))
print(len(s.value_counts(dropna=False)))
