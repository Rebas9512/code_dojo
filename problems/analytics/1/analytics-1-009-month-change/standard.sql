SELECT cur.month_start, cur.readers_n - prev.readers_n AS change
FROM monthly cur
LEFT JOIN monthly prev ON prev.month_start = cur.month_start - INTERVAL '1 month'
ORDER BY cur.month_start;
