WITH roster AS (
    SELECT DISTINCT user_id FROM logins WHERE logged_at >= DATE '2025-01-01' AND logged_at < DATE '2025-02-01'
), feb AS (
    SELECT DISTINCT user_id FROM logins WHERE logged_at >= DATE '2025-02-01' AND logged_at < DATE '2025-03-01'
)
SELECT COUNT(*) AS at_risk, COUNT(*) - COUNT(f.user_id) AS lost,
       ROUND((COUNT(*) - COUNT(f.user_id))::numeric / COUNT(*), 4) AS churn_rate
FROM roster r LEFT JOIN feb f USING (user_id);
