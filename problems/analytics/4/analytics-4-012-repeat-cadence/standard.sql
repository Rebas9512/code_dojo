WITH purchases AS (
    SELECT user_id,
           paid_at,
           LAG(paid_at) OVER (PARTITION BY user_id ORDER BY paid_at, payment_id) AS previous_at
    FROM payments
    WHERE amount > 0
)
SELECT user_id, ROUND(AVG(paid_at::date - previous_at::date), 2) AS mean_days
FROM purchases
WHERE previous_at IS NOT NULL
GROUP BY user_id
ORDER BY user_id;
