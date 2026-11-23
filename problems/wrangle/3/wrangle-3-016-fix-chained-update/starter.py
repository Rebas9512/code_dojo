def repair_stock(t):
    t[t['n'] < 0]['n'] = 0
    return t
