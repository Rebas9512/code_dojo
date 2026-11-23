WITH active AS (
    SELECT DISTINCT user_id FROM logins WHERE logged_at >= DATE '2025-02-01' AND logged_at < DATE '2025-03-01'
), money AS (
    SELECT user_id, SUM(amount) AS net, ____ FILTER (WHERE amount>0) AS charges FROM payments
    WHERE paid_at >= DATE '2025-02-01' AND paid_at < DATE '2025-03-01' GROUP BY user_id
)
SELECT ROUND(SUM(COALESCE(net, 0)) / COUNT(*), 2) AS arpu
FROM active LEFT JOIN money USING (user_id);
