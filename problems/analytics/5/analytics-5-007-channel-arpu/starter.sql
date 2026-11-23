WITH active AS (
    SELECT DISTINCT user_id FROM logins WHERE logged_at >= DATE '2025-02-01' AND logged_at < DATE '2025-03-01'
), money AS (
    SELECT user_id, SUM(amount) AS net, COUNT(*) FILTER (WHERE amount>0) AS charges FROM payments
    WHERE paid_at >= DATE '2025-02-01' AND paid_at < DATE '2025-03-01' GROUP BY user_id
)
SELECT channel, ROUND(SUM(COALESCE(net, 0)) / NULLIF(COUNT(money.user_id), 0), 2) AS arpu
FROM active LEFT JOIN money USING (user_id) JOIN readers USING (user_id) GROUP BY channel ORDER BY channel;
