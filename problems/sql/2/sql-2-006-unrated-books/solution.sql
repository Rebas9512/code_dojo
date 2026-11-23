SELECT b.book_id, b.title
FROM books b
LEFT JOIN ratings r ON r.book_id = b.book_id
WHERE r.book_id IS NULL;
