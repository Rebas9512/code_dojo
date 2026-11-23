SELECT a.month_start, ROUND((a.readers_n - b.readers_n)::numeric / NULLIF(a.readers_n, 0), 4) AS growth_rate
FROM monthly a LEFT JOIN monthly b ON b.month_start = a.month_start - INTERVAL '1 month'
ORDER BY a.month_start;
