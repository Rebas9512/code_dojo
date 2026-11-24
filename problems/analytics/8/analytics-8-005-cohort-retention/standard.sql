CREATE VIEW cohort_retention AS
WITH roster AS (
    SELECT user_id, DATE_TRUNC('week', joined_on)::date AS cohort_week
    FROM readers
)
SELECT r.cohort_week, COUNT(DISTINCT r.user_id) AS registered,
       COUNT(DISTINCT a.user_id) AS returned,
       ROUND(COUNT(DISTINCT a.user_id)::numeric / COUNT(DISTINCT r.user_id), 4) AS w1_rate
FROM roster r
LEFT JOIN clean_activity a ON a.user_id = r.user_id AND a.action = 'login'
    AND a.local_at >= r.cohort_week + 7 AND a.local_at < r.cohort_week + 14
WHERE r.cohort_week + 13 <= DATE '2025-03-15'
GROUP BY r.cohort_week;
