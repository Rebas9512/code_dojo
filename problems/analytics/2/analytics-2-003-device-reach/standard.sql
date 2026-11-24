SELECT device, COUNT(DISTINCT e.user_id) FILTER (WHERE e.action = 'order') AS order_users,
       COUNT(DISTINCT e.user_id) FILTER (WHERE e.action = 'pay') AS pay_users
FROM readers
LEFT JOIN events e USING (user_id)
GROUP BY device
ORDER BY device;
