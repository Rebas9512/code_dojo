def shift_log(t):
    return t.melt(id_vars='shop', value_vars=['am', 'pm'], var_name='shift', value_name='n')
