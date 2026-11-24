WITH days AS (
    SELECT DISTINCT user_id, logged_at::date AS day
    FROM logins
), labeled AS (
    SELECT user_id,
           day,
           day - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day)::integer AS segment
    FROM days
), runs AS (
    SELECT user_id, MIN(day) AS first_day, MAX(day) AS last_day, COUNT(*) AS days_n
    FROM labeled
    GROUP BY user_id, segment
), ranked AS (
    SELECT runs.*, DENSE_RANK() OVER (PARTITION BY user_id ORDER BY days_n DESC) AS place
    FROM runs
)
SELECT user_id, first_day, last_day
FROM ranked
WHERE place = 1
ORDER BY user_id, first_day;
