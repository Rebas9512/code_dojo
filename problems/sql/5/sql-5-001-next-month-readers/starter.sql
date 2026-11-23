WITH returnees AS (
    SELECT DISTINCT m.user_id FROM registration_months m
    JOIN reader_logins l ON l.user_id = m.user_id
     AND l.logged_on >= m.next_start AND l.logged_on < m.next_end
)
SELECT m.cohort, COUNT(*) AS readers, COUNT(r.user_id) AS returned,
       1.0 * ____ AS rate
FROM registration_months m LEFT JOIN returnees r ON r.user_id = m.user_id GROUP BY m.cohort;
