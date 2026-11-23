SELECT o.order_id, u.name
FROM orders o
JOIN users u ON u.user_id = o.user_id;
