INSERT INTO books (book_id, title, author_id, category, price, stock, publisher, published_on, pages) VALUES
    (31, 'Bulk Atlas', 7, 'history', 19.99, 1000, 'Northwind', '2025-01-01', 300),
    (32, 'Sold Out Again', 2, 'fantasy', 88.00, 0, 'Blue Kite', '2025-02-02', 350);
UPDATE books SET stock = 1 WHERE book_id = 1;
