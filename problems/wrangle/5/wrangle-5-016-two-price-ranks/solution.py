def two_ranks(shelf):
    prices = shelf.groupby('category')['price']
    shelf['place'] = prices.rank(method='min', ascending=False, na_option='bottom')
    shelf['tier'] = prices.rank(method='dense', ascending=False, na_option='bottom')
    return shelf[['category', 'book_id', 'place', 'tier']]
