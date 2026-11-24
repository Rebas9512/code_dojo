WITH device_sizes AS (
    SELECT device, COUNT(DISTINCT user_id) AS n
    FROM logins
    JOIN readers USING (user_id)
    WHERE logged_at >= DATE '2025-02-01' AND logged_at < DATE '2025-03-01'
    GROUP BY device
)
SELECT device, n, ROUND(n / SUM(n) OVER (), 4) AS share
FROM device_sizes
ORDER BY device;
