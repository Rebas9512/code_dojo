WITH last_seen AS (
    SELECT user_id, MAX(logged_at::date) AS last_day FROM logins
    WHERE logged_at::date <= DATE '2025-02-28' GROUP BY user_id
)
SELECT user_id, last_day FROM last_seen WHERE DATE '2025-02-28' - last_day >= 7 ORDER BY user_id;
