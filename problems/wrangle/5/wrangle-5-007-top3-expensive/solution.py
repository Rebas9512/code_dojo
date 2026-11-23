def display_three(books):
    ranked = books.sort_values(['price', 'book_id'], ascending=[False, True])
    return ranked.iloc[:3][['book_id', 'title', 'price']]
