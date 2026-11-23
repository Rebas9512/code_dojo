def shift_totals(t):
    p = t.pivot_table(index='shop', columns='shift', values='n', aggfunc=____, fill_value=0)
    return p.reset_index()
