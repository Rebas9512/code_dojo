import pandas as pd
t = pd.DataFrame({"p": [4, 9, 7]}, index=[1, 2, 3])
print(len(t.loc[1:2]))
print(len(t.iloc[1:2]))
