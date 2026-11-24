def shift_peaks(t):
    records = t.melt(id_vars='shop', var_name='shift', value_name='n')
    peaks = records.pivot_table(index='shop', columns='shift', values='n', aggfunc='max')
    return peaks.reset_index()
