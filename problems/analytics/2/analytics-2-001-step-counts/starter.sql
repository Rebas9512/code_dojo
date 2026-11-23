SELECT COUNT(____) FILTER (WHERE e.action = 'view') AS view_users,
       COUNT(DISTINCT e.user_id) FILTER (WHERE e.action = 'cart') AS cart_users,
       COUNT(DISTINCT e.user_id) FILTER (WHERE e.action = 'order') AS order_users
FROM events e;
