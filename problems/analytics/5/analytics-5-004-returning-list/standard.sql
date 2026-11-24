WITH activity AS (
    SELECT user_id, MIN(logged_at)::date AS first_day,
           COUNT(*) FILTER (WHERE logged_at >= DATE '2025-02-01' AND logged_at < DATE '2025-03-01') AS feb_visits,
           COUNT(*) FILTER (WHERE logged_at >= DATE '2025-03-01') AS mar_visits
    FROM logins
    WHERE logged_at < DATE '2025-04-01'
    GROUP BY user_id
)
SELECT user_id
FROM activity
WHERE first_day < DATE '2025-02-01' AND feb_visits = 0 AND mar_visits > 0
ORDER BY user_id;
