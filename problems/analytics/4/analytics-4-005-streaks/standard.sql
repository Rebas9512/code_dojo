WITH days AS (
    SELECT DISTINCT user_id, logged_at::date AS day
    FROM logins
), labeled AS (
    SELECT user_id,
           day,
           day - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day)::integer AS segment
    FROM days
)
SELECT user_id, MIN(day) AS first_day, MAX(day) AS last_day, COUNT(*) AS days_n
FROM labeled
GROUP BY user_id, segment
ORDER BY user_id, first_day;
