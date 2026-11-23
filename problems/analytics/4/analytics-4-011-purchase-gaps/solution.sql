WITH purchases AS (
    SELECT user_id, payment_id, paid_at,
           LAG(paid_at) OVER (PARTITION BY user_id ORDER BY paid_at, payment_id) AS previous_at
    FROM payments WHERE amount>0
)
SELECT user_id, payment_id, paid_at::date - previous_at::date AS gap_days FROM purchases WHERE previous_at IS NOT NULL ORDER BY user_id, paid_at, payment_id;
