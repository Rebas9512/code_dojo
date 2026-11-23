WITH login_days AS (
    SELECT DISTINCT user_id, logged_on AS day
    FROM reader_logins
    WHERE logged_on <= DATE '2025-03-31'
), tagged AS (
    SELECT user_id, day,
           (day - DATE '2000-01-01') - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS block,
           MAX(day) OVER (PARTITION BY user_id) AS last_seen
    FROM login_days
), runs AS (
    SELECT user_id, MIN(day) AS start_day, MAX(day) AS end_day, COUNT(*) AS length
    FROM tagged
    WHERE last_seen < DATE '2025-03-01'
    GROUP BY user_id, block
), ranked AS (
    SELECT runs.*, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY length DESC, start_day) AS pos
    FROM runs
)
SELECT user_id, start_day, end_day, length
FROM ranked
WHERE pos = 1;
