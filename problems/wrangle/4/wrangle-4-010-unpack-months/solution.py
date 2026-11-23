def month_log(t):
    long = t.melt(id_vars='shop', value_vars=['jan', 'feb'], var_name='month', value_name='qty')
    return long.groupby(['shop','month'], as_index=False).agg(qty=('qty','sum'))
