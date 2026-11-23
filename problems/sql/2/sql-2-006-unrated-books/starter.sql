SELECT b.book_id, b.title
FROM books b
LEFT JOIN ratings r ON r.book_id = b.book_id
WHERE r.review IS NULL;
