import pandas as pd


def months(t):
    return pd.to_datetime(t['day']).dt.month
