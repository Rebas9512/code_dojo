SELECT bench, SUM(sheets) AS total
FROM load_slips
GROUP BY bench
ORDER BY total DESC, bench
LIMIT 1
OFFSET 2;
