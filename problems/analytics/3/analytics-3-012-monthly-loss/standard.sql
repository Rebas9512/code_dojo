WITH jan_readers AS (
    SELECT DISTINCT user_id
    FROM logins
    WHERE logged_at >= DATE '2025-01-01' AND logged_at < DATE '2025-02-01'
), feb_readers AS (
    SELECT DISTINCT user_id
    FROM logins
    WHERE logged_at >= DATE '2025-02-01' AND logged_at < DATE '2025-03-01'
), counts AS (
    SELECT COUNT(*) AS at_risk, COUNT(*) - COUNT(f.user_id) AS lost
    FROM jan_readers
    LEFT JOIN feb_readers f USING (user_id)
)
SELECT at_risk, lost, ROUND(lost::numeric / at_risk, 4) AS churn_rate
FROM counts;
