def repair_stock(t):
    t.loc[t['n'] < 0, 'n'] = 0
    return t
