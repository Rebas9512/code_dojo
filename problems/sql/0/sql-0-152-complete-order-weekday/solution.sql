SELECT order_id, EXTRACT(DOW FROM order_date) AS weekday
FROM orders;
