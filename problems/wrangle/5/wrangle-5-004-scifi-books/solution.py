def scifi_list(books):
    return books.loc[books['category'] == 'scifi', ['book_id', 'title']]
