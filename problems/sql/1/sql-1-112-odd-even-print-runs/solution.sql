SELECT day, SUM(CASE WHEN copies % 2 = 1 THEN copies ELSE 0 END) AS odd_copies,
       SUM(CASE WHEN copies % 2 = 0 THEN copies ELSE 0 END) AS even_copies
FROM press_runs GROUP BY day ORDER BY day;
