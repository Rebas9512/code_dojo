SELECT u.user_id, c.category, COUNT(DISTINCT p.order_id) AS order_count
FROM users u
CROSS JOIN categories c
LEFT JOIN purchases p ON p.user_id = u.user_id AND p.category = c.category
GROUP BY u.user_id, c.category;
