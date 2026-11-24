WITH days AS (
    SELECT DISTINCT user_id, logged_at::date AS day
    FROM logins
), labeled AS (
    SELECT user_id,
           day,
           day - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day)::integer AS segment
    FROM days
), runs AS (
    SELECT user_id, MIN(day) AS first_day, COUNT(*) AS days_n
    FROM labeled
    GROUP BY user_id, segment
)
SELECT user_id, first_day, days_n
FROM runs
WHERE days_n >= 3
ORDER BY user_id, first_day;
