from io import StringIO

import pandas as pd


def read_stock(text):
    inventory = pd.read_csv(StringIO(text), sep=';')
    return inventory['stock']
