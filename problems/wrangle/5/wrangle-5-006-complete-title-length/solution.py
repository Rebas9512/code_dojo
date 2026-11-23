def title_lengths(books):
    books['chars'] = books['title'].apply(len)
    return books[['book_id', 'chars']]
