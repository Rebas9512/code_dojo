INSERT INTO books (book_id, title, author_id, category, price, stock, publisher, published_on, pages) VALUES
    (31, 'Self Published Notes', 9, 'fiction', 12.00, 2, NULL, NULL, 80),
    (32, 'Harbor Classics', 1, 'fiction', 30.00, 2, 'Harbor Press', '2025-01-01', 300);
UPDATE books SET publisher = NULL WHERE book_id = 2;
