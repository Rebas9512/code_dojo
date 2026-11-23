import pandas as pd
t = pd.DataFrame({"n": [3, 1], "p": [2, 8]})
t["total"] = t["n"] * t["p"]
print(t["total"].tolist())
