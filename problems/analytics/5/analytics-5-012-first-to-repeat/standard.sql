WITH purchases AS (
    SELECT user_id, paid_at::date AS second_day,
           LAG(paid_at::date) OVER (PARTITION BY user_id ORDER BY paid_at, payment_id) AS first_day,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY paid_at, payment_id) AS purchase_no
    FROM payments
    WHERE amount > 0
)
SELECT user_id, first_day, second_day, second_day - first_day AS gap
FROM purchases
WHERE purchase_no = 2
ORDER BY user_id;
