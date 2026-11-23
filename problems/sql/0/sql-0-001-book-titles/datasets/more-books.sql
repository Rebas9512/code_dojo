-- 多两本书：一本同名不同版，一本没有作者 / 出版信息
INSERT INTO books (book_id, title, author_id, category, price, stock, publisher, published_on, pages) VALUES
    (31, 'Data at Dawn', 8, 'programming', 52.00, 1, 'Harbor Press', '2025-06-01', 310),
    (32, 'The Quiet Hours', NULL, 'fiction', 26.00, 5, NULL, NULL, 200);
