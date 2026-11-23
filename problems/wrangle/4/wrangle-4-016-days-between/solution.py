import pandas as pd


def elapsed(loans, returns):
    paired = loans.merge(returns, on='id')
    start = pd.to_datetime(paired['start'])
    end = pd.to_datetime(paired['end'])
    paired['days'] = (end - start).dt.days
    return paired[['id', 'days']]
