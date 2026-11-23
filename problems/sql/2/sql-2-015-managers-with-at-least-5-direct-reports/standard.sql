SELECT m.name
FROM crew m
JOIN crew e ON e.leader_id = m.person_id
GROUP BY m.person_id, m.name
HAVING COUNT(*) >= 5;
