SELECT u.user_id, COALESCE(c.n, 0) AS order_count
FROM users u
LEFT JOIN order_counts c ON c.user_id = u.user_id;
