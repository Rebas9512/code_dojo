WITH cohorts AS (
    SELECT user_id, DATE_TRUNC('week', joined_on)::date AS cohort FROM readers
), marks AS (
    SELECT c.cohort, c.user_id,
           (DATE_TRUNC('week', l.logged_at)::date - c.cohort) / 7 AS wk
    FROM cohorts c LEFT JOIN logins l USING (user_id)
    WHERE c.cohort + 20 <= DATE '2025-03-14'
)
SELECT cohort, COUNT(DISTINCT user_id) FILTER (WHERE wk=1) AS w1
FROM marks GROUP BY cohort ORDER BY cohort;
