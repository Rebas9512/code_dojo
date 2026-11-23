WITH days AS (
    SELECT DISTINCT user_id, logged_at::date AS day FROM logins
), labeled AS (
    SELECT user_id, day, day - ____::integer AS segment FROM days
), runs AS (
    SELECT user_id, MIN(day) AS first_day, MAX(day) AS last_day, COUNT(*) AS days_n
    FROM labeled GROUP BY user_id, segment
)
SELECT user_id, first_day, last_day, days_n FROM runs ORDER BY user_id, first_day;
