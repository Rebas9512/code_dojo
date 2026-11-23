SELECT m.person_id, m.name, COUNT(*) AS reports, ROUND(AVG(e.age), 0) AS mean_age
FROM team m
JOIN team e ON e.leader_id = m.person_id
GROUP BY m.person_id, m.name
ORDER BY m.person_id;
