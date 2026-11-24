WITH days AS (
    SELECT GENERATE_SERIES(DATE '2025-01-01', DATE '2025-01-14', INTERVAL '1 day')::date AS day
), daily_visits AS (
    SELECT day, COUNT(l.login_id) AS visits
    FROM days
    LEFT JOIN logins l
        ON l.logged_at::date = day
    GROUP BY day
)
SELECT day
FROM daily_visits
WHERE visits = 0
ORDER BY day;
