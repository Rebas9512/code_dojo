def top_tiers(shelf):
    known = shelf.dropna(subset=['price'])
    tier = known.groupby('category')['price'].rank(method='dense', ascending=False)
    return known.loc[tier <= 2, ['book_id', 'category', 'price']]
