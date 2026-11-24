import pandas as pd


def status_counts(t, month):
    in_month = pd.to_datetime(t['day']).dt.month == month
    statuses = t.loc[in_month, 'status'].fillna('unrecorded')
    return statuses.value_counts().reset_index(name='orders')
