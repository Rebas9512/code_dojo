WITH days AS (
    SELECT GENERATE_SERIES(DATE '2025-01-01', DATE '2025-01-07', INTERVAL '1 day')::date AS day
)
SELECT day, COUNT(DISTINCT logins.user_id) AS dau
FROM days
LEFT JOIN logins ON logins.logged_at::date = day
GROUP BY day
ORDER BY day;
