SELECT order_month, author_id, SUM(line_amount) AS author_revenue
FROM line_amounts
WHERE author_id IS NOT NULL
GROUP BY order_month, author_id
