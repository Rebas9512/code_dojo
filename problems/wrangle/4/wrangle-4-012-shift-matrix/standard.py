def shift_totals(t):
    totals = t.pivot_table(index='shop', columns='shift', values='n', aggfunc='sum', fill_value=0)
    return totals.reset_index()
