import pandas as pd
t = pd.DataFrame({"id": [8, 2, 4], "p": [3, 3, 5]})
print(t.sort_values(["p", "id"], ascending=[False, True])["id"].tolist())
