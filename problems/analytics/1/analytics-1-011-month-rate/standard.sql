SELECT cur.month_start, ROUND((cur.readers_n - prev.readers_n)::numeric / NULLIF(prev.readers_n, 0), 4) AS growth_rate
FROM monthly cur
LEFT JOIN monthly prev ON prev.month_start = cur.month_start - INTERVAL '1 month'
ORDER BY cur.month_start;
