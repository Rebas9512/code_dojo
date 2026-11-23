SELECT category, book_id,
       ROW_NUMBER() OVER (____ ORDER BY price DESC NULLS LAST, book_id) AS position
FROM shelf;
