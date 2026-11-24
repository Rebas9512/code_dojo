SELECT channel,
       COUNT(DISTINCT user_id) FILTER (WHERE logged_at >= DATE '2025-03-01')
       - COUNT(DISTINCT user_id) FILTER (WHERE logged_at < DATE '2025-03-01') AS net
FROM logins
JOIN readers USING (user_id)
WHERE logged_at >= DATE '2025-02-01' AND logged_at < DATE '2025-04-01'
GROUP BY channel
ORDER BY channel;
