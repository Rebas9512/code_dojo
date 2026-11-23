SELECT MAX(n) AS most_orders
FROM (SELECT user_id, COUNT(*) AS n FROM orders GROUP BY user_id) AS counts;
