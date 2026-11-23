import pandas as pd


def phone_totals(users):
    known = users.dropna(subset=['phone'])
    return pd.DataFrame({'users_total': [len(users)], 'with_phone': [len(known)]})
