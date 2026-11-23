SELECT category, COUNT(*) AS book_count
FROM books
GROUP BY category;
