def shift_peaks(t):
    long = t.melt(id_vars='shop', var_name='shift', value_name='n')
    p = long.pivot_table(index='shop', columns='shift', values='n', aggfunc='max', fill_value=0)
    return p.reset_index()
