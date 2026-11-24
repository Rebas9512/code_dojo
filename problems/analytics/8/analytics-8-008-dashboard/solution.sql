WITH reach AS (
    SELECT COALESCE(MAX(active_users) FILTER (WHERE grain = 'day' AND period_start = DATE '2025-03-15'), 0) AS dau,
           COALESCE(MAX(active_users) FILTER (WHERE grain = 'week' AND period_start = DATE '2025-03-10'), 0) AS wau
    FROM active_reach
), sessions AS (
    SELECT COUNT(*) AS sessions_wtd
    FROM app_sessions
    WHERE started_at >= DATE '2025-03-10'
), latest_cohort AS (
    SELECT cohort_week, w1_rate
    FROM cohort_retention
    ORDER BY cohort_week DESC
    LIMIT 1
), experiment AS (
    SELECT MAX(buy_rate) FILTER (WHERE arm = 'A') AS cover_a,
           MAX(buy_rate) FILTER (WHERE arm = 'B') AS cover_b
    FROM cover_readout
)
SELECT DATE '2025-03-15' AS as_of, r.dau, r.wau, s.sessions_wtd, f.order_rate,
       c.cohort_week, c.w1_rate, g.new_users + g.reactivated - g.lost AS net_active,
       e.cover_a, e.cover_b
FROM monthly_growth g
CROSS JOIN reach r
CROSS JOIN sessions s
CROSS JOIN order_funnel f
CROSS JOIN experiment e
LEFT JOIN latest_cohort c ON TRUE
WHERE g.month_start = DATE '2025-03-01';
