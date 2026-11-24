import pandas as pd


def phone_totals(users):
    with_phone = len(users['phone'].dropna())
    return pd.DataFrame({'users_total': [len(users)], 'with_phone': [with_phone]})
