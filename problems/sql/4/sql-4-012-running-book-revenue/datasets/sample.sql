CREATE VIEW daily_sales AS
SELECT o.order_date AS day, SUM(i.quantity * i.unit_price) AS amount
FROM orders o JOIN order_items i ON i.order_id = o.order_id
WHERE o.status <> 'cancelled' GROUP BY o.order_date;
