def available(t):
    return t.loc[t['stock'] > 0, ['id']]
