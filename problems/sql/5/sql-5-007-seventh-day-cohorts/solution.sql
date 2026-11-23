WITH cohorts AS (
    SELECT user_id, MIN(logged_on) AS first_day FROM reader_logins GROUP BY user_id
), active_days AS (SELECT DISTINCT user_id, logged_on FROM reader_logins)
SELECT c.first_day, COUNT(*) AS readers, COUNT(a.user_id) AS returned,
       1.0 * COUNT(a.user_id) / COUNT(*) AS rate
FROM cohorts c LEFT JOIN active_days a ON a.user_id = c.user_id AND a.logged_on = c.first_day + 7
GROUP BY c.first_day;
