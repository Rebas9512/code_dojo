def shelf_positions(shelf):
    ranked = shelf.sort_values(['price', 'book_id'], ascending=[False, True])
    ranked['position'] = ranked.groupby('category').cumcount() + 1
    return ranked[['category', 'book_id', 'position']]
