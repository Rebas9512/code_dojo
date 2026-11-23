from io import StringIO

import pandas as pd


def after_delivery(text, extra):
    t = pd.read_csv(StringIO(text), dtype={'n': 'string'})
    return t['n'].astype('Int64') + extra
