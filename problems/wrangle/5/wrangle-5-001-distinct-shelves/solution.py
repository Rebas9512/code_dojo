import pandas as pd
books = pd.DataFrame({"category":["scifi","kids","scifi","history"]})
out = books[["category"]].drop_duplicates()
print(out["category"].tolist())
