SELECT DATE_TRUNC('week', logged_at)::date AS period, COUNT(DISTINCT user_id) AS active
FROM logins
GROUP BY period
ORDER BY period;
