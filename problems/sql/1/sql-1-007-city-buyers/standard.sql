SELECT city, COUNT(DISTINCT user_id) AS buyers
FROM buyer_orders
GROUP BY city;
