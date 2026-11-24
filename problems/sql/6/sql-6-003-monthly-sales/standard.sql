SELECT o.order_month, COUNT(DISTINCT o.order_id) AS order_count,
       COALESCE(SUM(i.line_amount), 0) AS revenue
FROM valid_orders AS o
LEFT JOIN line_amounts AS i ON i.order_id = o.order_id
GROUP BY o.order_month
