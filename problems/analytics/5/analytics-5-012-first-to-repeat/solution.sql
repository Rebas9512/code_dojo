WITH numbered AS (
    SELECT user_id, paid_at::date AS day,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY paid_at, payment_id) AS n
    FROM payments WHERE amount>0
), pairs AS (
    SELECT user_id, MIN(day) AS first_day, MAX(day) AS second_day FROM numbered
    WHERE n<=2 GROUP BY user_id HAVING COUNT(*)=2
)
SELECT user_id, first_day, second_day, second_day-first_day AS gap FROM pairs ORDER BY user_id;
