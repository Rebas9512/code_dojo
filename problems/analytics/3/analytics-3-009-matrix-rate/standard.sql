WITH cohorts AS (
    SELECT user_id, DATE_TRUNC('week', joined_on)::date AS cohort
    FROM readers
), login_weeks AS (
    SELECT c.cohort,
           c.user_id,
           (DATE_TRUNC('week', l.logged_at)::date - c.cohort) / 7 AS week_number
    FROM cohorts c
    LEFT JOIN logins l USING (user_id)
    WHERE c.cohort + 20 <= DATE '2025-03-14'
)
SELECT cohort,
       ROUND(COUNT(DISTINCT user_id) FILTER (WHERE week_number = 2)::numeric / COUNT(DISTINCT user_id), 4) AS w2_rate
FROM login_weeks
GROUP BY cohort
ORDER BY cohort;
