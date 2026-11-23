SELECT title,
       price,
       CASE
           WHEN price < 30 THEN 'budget'
           WHEN price < 50 THEN 'standard'
           ELSE 'premium'
       END AS price_band
FROM books;
