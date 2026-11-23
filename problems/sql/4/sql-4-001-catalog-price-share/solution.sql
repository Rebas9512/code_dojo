SELECT book_id, price / NULLIF(SUM(price) OVER (), 0) AS share
FROM shelf;
