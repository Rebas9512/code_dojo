SELECT sold_on, STRING_AGG(DISTINCT title, ',' ORDER BY title) AS titles
FROM sold_titles
GROUP BY sold_on;
