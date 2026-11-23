def stock_value(books):
    books['stock_value'] = books['price'] * books['stock']
    return books[['title', 'stock_value']]
