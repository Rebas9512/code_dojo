import pandas as pd
s = pd.Series(["2025-12-31", "2026-01-01"])
print(pd.to_datetime(s).dt.month.tolist())
