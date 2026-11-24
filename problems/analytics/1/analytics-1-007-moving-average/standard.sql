WITH days AS (
    SELECT GENERATE_SERIES(DATE '2025-01-01', DATE '2025-01-14', INTERVAL '1 day')::date AS day
), daily AS (
    SELECT day, COUNT(DISTINCT logins.user_id) AS dau
    FROM days
    LEFT JOIN logins ON logins.logged_at::date = day
    GROUP BY day
), rolling AS (
    SELECT day, AVG(dau) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS mean_dau
    FROM daily
)
SELECT day, ROUND(mean_dau, 2) AS mean_dau
FROM rolling
WHERE day >= DATE '2025-01-07'
ORDER BY day;
