SELECT DISTINCT user_id
FROM orders
WHERE status <> 'cancelled'
  AND order_date BETWEEN '2025-01-01' AND '2025-06-30'
ORDER BY user_id;
