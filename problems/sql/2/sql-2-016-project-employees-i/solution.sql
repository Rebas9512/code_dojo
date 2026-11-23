SELECT a.project_id, ROUND(AVG(p.years), 2) AS mean_years
FROM assignments a
JOIN people p ON p.person_id = a.person_id
GROUP BY a.project_id;
