def matched(books, lots):
    return books.merge(lots, on='id', how='inner')
