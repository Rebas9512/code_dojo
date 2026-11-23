WITH days AS (
    SELECT DISTINCT user_id, order_date AS day
    FROM orders
), tagged_days AS (
    SELECT user_id, day, (day - DATE '2000-01-01')
           - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS block
    FROM days
)
SELECT user_id, MIN(day) AS start_day, MAX(day) AS end_day, COUNT(*) AS days
FROM tagged_days
GROUP BY user_id, block;
