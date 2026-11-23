SELECT category, book_id,
       ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC NULLS LAST, book_id) AS position
FROM shelf;
