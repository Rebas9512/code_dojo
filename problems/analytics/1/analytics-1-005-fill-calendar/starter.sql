WITH days AS (
    SELECT generate_series(DATE '2025-01-01', DATE '2025-01-14', INTERVAL '1 day')::date AS day
), daily AS (
    SELECT day, COUNT(DISTINCT l.user_id) AS dau
    FROM days ____ logins l ON l.logged_at::date = day GROUP BY day
)
SELECT day, dau FROM daily ORDER BY day;
