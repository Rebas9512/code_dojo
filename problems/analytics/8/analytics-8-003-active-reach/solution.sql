CREATE VIEW active_reach AS
WITH periods(grain) AS (
    VALUES ('day'), ('week')
)
SELECT grain, DATE_TRUNC(grain, local_at)::date AS period_start,
       COUNT(DISTINCT user_id) AS active_users
FROM clean_activity
CROSS JOIN periods
WHERE action = 'login'
GROUP BY grain, period_start;
