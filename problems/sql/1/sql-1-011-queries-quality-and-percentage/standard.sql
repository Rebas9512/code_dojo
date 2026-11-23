SELECT term, ROUND(AVG(rating::numeric / position), 2) AS quality,
       ROUND(AVG(CASE WHEN rating < 3 THEN 100 ELSE 0 END), 2) AS poor_pct
FROM search_hits
GROUP BY term;
