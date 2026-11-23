SELECT order_id, EXTRACT(____ FROM order_date) AS weekday
FROM orders;
