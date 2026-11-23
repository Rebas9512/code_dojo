CREATE VIEW daily_sales AS
SELECT o.order_date AS day, SUM(i.quantity * i.unit_price) AS amount
FROM orders o JOIN order_items i ON i.order_id = o.order_id
WHERE o.status <> 'cancelled' GROUP BY o.order_date;
CREATE VIEW shop_calendar AS
SELECT dates.d::date AS day, COALESCE(s.amount, 0) AS amount
FROM generate_series((SELECT MIN(day) FROM daily_sales)::timestamp,
                     (SELECT MAX(day) FROM daily_sales)::timestamp, INTERVAL '1 day') AS dates(d)
LEFT JOIN daily_sales s ON s.day = dates.d::date;
