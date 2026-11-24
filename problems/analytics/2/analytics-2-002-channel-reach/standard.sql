SELECT channel, COUNT(DISTINCT e.user_id) FILTER (WHERE e.action = 'view') AS view_users,
       COUNT(DISTINCT e.user_id) FILTER (WHERE e.action = 'cart') AS cart_users
FROM readers
LEFT JOIN events e USING (user_id)
GROUP BY channel
ORDER BY channel;
