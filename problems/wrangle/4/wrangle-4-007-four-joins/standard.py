def reconcile(books, lots, how):
    return books.merge(lots, on='id', how=how)
