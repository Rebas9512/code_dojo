WITH sizes AS (SELECT device, COUNT(*) AS n FROM readers JOIN (SELECT DISTINCT user_id FROM logins WHERE logged_at >= DATE '2025-02-01' AND logged_at < DATE '2025-03-01') a USING (user_id) GROUP BY device)
SELECT device, n, ROUND(n / SUM(n) OVER (), 4) AS share FROM sizes ORDER BY device;
