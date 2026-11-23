SELECT user_id,
       SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS delivered_count,
       SUM(____) AS cancelled_count
FROM orders
GROUP BY user_id;
