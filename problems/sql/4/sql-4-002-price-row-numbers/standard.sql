SELECT book_id, ROW_NUMBER() OVER (ORDER BY price DESC NULLS LAST, book_id) AS position
FROM shelf;
