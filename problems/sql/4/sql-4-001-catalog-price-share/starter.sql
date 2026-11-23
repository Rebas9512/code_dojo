SELECT book_id, price / NULLIF(SUM(price) ____, 0) AS share
FROM shelf;
