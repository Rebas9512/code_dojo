def big_categories(books):
    counts = books['category'].value_counts().reset_index(name='book_count')
    return counts.loc[counts['book_count'] >= 5]
