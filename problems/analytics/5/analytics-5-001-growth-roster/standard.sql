WITH activity AS (
    SELECT user_id, MIN(logged_at)::date AS first_day,
           COUNT(*) FILTER (WHERE logged_at >= DATE '2025-02-01' AND logged_at < DATE '2025-03-01') AS feb_visits,
           COUNT(*) FILTER (WHERE logged_at >= DATE '2025-03-01') AS mar_visits
    FROM logins
    WHERE logged_at < DATE '2025-04-01'
    GROUP BY user_id
)
SELECT user_id,
       CASE WHEN mar_visits = 0 THEN 'lost'
            WHEN feb_visits > 0 THEN 'retained'
            WHEN first_day >= DATE '2025-03-01' THEN 'new'
            ELSE 'reactivated' END AS status
FROM activity
WHERE feb_visits > 0 OR mar_visits > 0
ORDER BY user_id;
