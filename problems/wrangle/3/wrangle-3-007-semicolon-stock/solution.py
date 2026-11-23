from io import StringIO

import pandas as pd


def read_stock(text):
    t = pd.read_csv(StringIO(text), sep=';')
    return t['stock']
