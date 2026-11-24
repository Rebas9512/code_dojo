def priced(t):
    priced_books = t.dropna(subset=['price'])
    priced_books['cents'] = priced_books['price'] * 100
    return priced_books
