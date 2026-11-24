def month_log(t):
    monthly = t.melt(id_vars='shop', value_vars=['jan', 'feb'], var_name='month', value_name='qty')
    return monthly.groupby(['shop', 'month'], as_index=False).agg(qty=('qty', 'sum'))
