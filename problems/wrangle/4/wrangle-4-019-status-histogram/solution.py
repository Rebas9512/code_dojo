import pandas as pd


def status_counts(t, month):
    in_month = pd.to_datetime(t['day']).dt.month == month
    s = t.loc[in_month, 'status'].fillna('unrecorded')
    return s.value_counts().reset_index(name='orders')
