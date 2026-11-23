SELECT book_id, price
FROM books
WHERE price > (SELECT AVG(price) FROM books);
