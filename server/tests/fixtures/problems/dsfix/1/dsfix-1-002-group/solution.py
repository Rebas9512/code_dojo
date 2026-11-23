import pandas as pd

def totals(rows):
    table = pd.DataFrame(rows, columns=["组", "总数"])
    return table.groupby("组", as_index=False).sum()
