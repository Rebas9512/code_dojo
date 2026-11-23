SELECT title,
       CASE
           WHEN stock = 0 THEN 'sold out'
           WHEN ____ THEN 'low'
           ELSE 'in stock'
       END AS stock_label
FROM books;
