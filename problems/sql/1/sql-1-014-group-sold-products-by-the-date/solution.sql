SELECT sold_on, COUNT(DISTINCT item) AS varieties,
       STRING_AGG(DISTINCT item, ',' ORDER BY item) AS items
FROM receipts
GROUP BY sold_on
ORDER BY sold_on;
