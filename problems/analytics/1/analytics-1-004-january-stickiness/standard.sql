SELECT COUNT(DISTINCT user_id) FILTER (WHERE logged_at::date = DATE '2025-01-31') AS dau,
       COUNT(DISTINCT user_id) AS mau,
       ROUND(COUNT(DISTINCT user_id) FILTER (WHERE logged_at::date = DATE '2025-01-31')::numeric
             / NULLIF(COUNT(DISTINCT user_id), 0), 4) AS stickiness
FROM logins
WHERE logged_at >= DATE '2025-01-01' AND logged_at < DATE '2025-02-01';
