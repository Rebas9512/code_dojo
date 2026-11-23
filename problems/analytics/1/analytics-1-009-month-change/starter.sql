SELECT a.month_start, a.readers_n - b.readers_n AS change
FROM monthly a LEFT JOIN monthly b ON b.month_start = a.month_start - ____
ORDER BY a.month_start;
