from io import StringIO

import pandas as pd


def restock(text):
    t = pd.read_csv(StringIO(text))
    kept = t.loc[t['stock'] > 0]
    return kept.sort_values(['stock', 'id'])
