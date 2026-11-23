SELECT book_id, 1.0 * SUM(returned) / NULLIF(SUM(sold), 0) AS return_rate
FROM stock_checks
GROUP BY book_id;
