import pandas as pd


def revenue(daily_sales):
    daily_sales['date_key'] = pd.to_datetime(daily_sales['day'])
    out = daily_sales.sort_values('date_key')
    out['total'] = out['amount'].cumsum()
    return out[['day', 'amount', 'total']]
