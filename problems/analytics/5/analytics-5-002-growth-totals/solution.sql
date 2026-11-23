WITH months AS (
    SELECT generate_series(DATE '2025-01-01', DATE '2025-03-01', INTERVAL '1 month')::date AS month_start
), flags AS (
    SELECT m.month_start, l.user_id, MIN(l.logged_at)::date AS first_day,
           COUNT(*) FILTER (WHERE l.logged_at >= m.month_start - INTERVAL '1 month'
                              AND l.logged_at < m.month_start) AS prev_n,
           COUNT(*) FILTER (WHERE l.logged_at >= m.month_start) AS now_n
    FROM months m JOIN logins l ON l.logged_at < m.month_start + INTERVAL '1 month'
    GROUP BY m.month_start, l.user_id
), ledger AS (
    SELECT month_start, CASE WHEN now_n=0 THEN 'lost' WHEN prev_n>0 THEN 'retained'
                             WHEN first_day >= month_start THEN 'new' ELSE 'reactivated' END AS status
    FROM flags WHERE prev_n>0 OR now_n>0
)
SELECT m.month_start,
       COUNT(*) FILTER (WHERE status='new') AS new_n,
       COUNT(*) FILTER (WHERE status='retained') AS retained_n,
       COUNT(*) FILTER (WHERE status='reactivated') AS reactivated_n,
       COUNT(*) FILTER (WHERE status='lost') AS lost_n
FROM months m LEFT JOIN ledger USING (month_start) GROUP BY m.month_start ORDER BY m.month_start;
