SELECT book_id, ____ OVER (ORDER BY price DESC NULLS LAST, book_id) AS position
FROM shelf;
