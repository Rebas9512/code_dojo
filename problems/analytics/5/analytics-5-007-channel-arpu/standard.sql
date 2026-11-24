WITH active AS (
    SELECT DISTINCT user_id
    FROM logins
    WHERE logged_at >= DATE '2025-02-01' AND logged_at < DATE '2025-03-01'
), monthly_payments AS (
    SELECT user_id, SUM(amount) AS net
    FROM payments
    WHERE paid_at >= DATE '2025-02-01' AND paid_at < DATE '2025-03-01'
    GROUP BY user_id
)
SELECT channel, ROUND(AVG(COALESCE(net, 0)), 2) AS arpu
FROM active
LEFT JOIN monthly_payments USING (user_id)
JOIN readers USING (user_id)
GROUP BY channel
ORDER BY channel;
