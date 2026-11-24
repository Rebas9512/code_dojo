SELECT DATE_TRUNC('week', joined_on)::date AS cohort, COUNT(*) AS readers_n
FROM readers
GROUP BY cohort
ORDER BY cohort;
