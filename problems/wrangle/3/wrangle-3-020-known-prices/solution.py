def priced(t):
    t['cents'] = t['price'] * 100
    return t.dropna(subset=['price'])
