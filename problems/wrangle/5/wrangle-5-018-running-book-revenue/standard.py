def revenue(daily_sales):
    ordered = daily_sales.sort_values('day')
    ordered['total'] = ordered['amount'].cumsum()
    return ordered[['day', 'amount', 'total']]
