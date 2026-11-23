SELECT DATE_TRUNC('day', logged_at)::date AS period, COUNT(____) AS active
FROM logins GROUP BY period ORDER BY period;
