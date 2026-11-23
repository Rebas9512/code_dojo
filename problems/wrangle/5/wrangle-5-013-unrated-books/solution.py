def unrated(books, ratings):
    rated = books['book_id'].isin(ratings['book_id'])
    return books.loc[rated.eq(False), ['book_id', 'title']]
