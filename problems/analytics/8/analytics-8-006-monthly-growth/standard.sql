CREATE VIEW monthly_growth AS
WITH months AS (
    SELECT GENERATE_SERIES(DATE '2025-01-01', DATE '2025-03-01', INTERVAL '1 month')::date AS month_start
), visits AS (
    SELECT DISTINCT user_id, DATE_TRUNC('month', local_at)::date AS active_month
    FROM clean_activity
    WHERE action = 'login'
), history AS (
    SELECT m.month_start, v.user_id, MIN(v.active_month) AS first_month,
           BOOL_OR(v.active_month = m.month_start) AS active_now,
           BOOL_OR(v.active_month = m.month_start - INTERVAL '1 month') AS active_before
    FROM months m
    JOIN visits v ON v.active_month <= m.month_start
    GROUP BY m.month_start, v.user_id
)
SELECT m.month_start,
       COUNT(*) FILTER (WHERE h.first_month = m.month_start) AS new_users,
       COUNT(*) FILTER (WHERE h.active_now AND h.active_before) AS retained,
       COUNT(*) FILTER (WHERE h.active_now AND NOT h.active_before AND h.first_month < m.month_start) AS reactivated,
       COUNT(*) FILTER (WHERE h.active_before AND NOT h.active_now) AS lost
FROM months m
LEFT JOIN history h USING (month_start)
GROUP BY m.month_start;
