SELECT s.machine_id, ROUND(AVG(e.moment - s.moment), 3) AS mean_seconds
FROM events s
JOIN events e ON e.machine_id = s.machine_id AND e.batch_id = s.batch_id
WHERE s.kind = 'start' AND e.kind = 'end'
GROUP BY s.machine_id;
