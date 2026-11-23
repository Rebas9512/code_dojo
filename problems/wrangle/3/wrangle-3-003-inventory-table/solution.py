import pandas as pd


def inventory(rows):
    return pd.DataFrame(rows, columns=['shelf', 'stock'])
