WITH days AS (
    SELECT generate_series(DATE '2025-01-01', DATE '2025-01-14', INTERVAL '1 day')::date AS day
), daily AS (
    SELECT day, COUNT(DISTINCT l.user_id) AS dau
    FROM days LEFT JOIN logins l ON l.logged_at::date = day GROUP BY day
)
SELECT day, dau FROM daily WHERE day <= DATE '2025-01-07' ORDER BY day;
