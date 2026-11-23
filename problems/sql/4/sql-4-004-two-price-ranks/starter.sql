SELECT category, book_id,
       DENSE_RANK() OVER (PARTITION BY category ORDER BY price DESC NULLS LAST) AS place,
       DENSE_RANK() OVER (PARTITION BY category ORDER BY price DESC NULLS LAST) AS tier
FROM shelf;
