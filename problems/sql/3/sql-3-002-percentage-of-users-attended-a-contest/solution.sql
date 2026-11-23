SELECT event_id, 100.0 * COUNT(*) / (SELECT COUNT(*) FROM members) AS percentage
FROM signups GROUP BY event_id
ORDER BY percentage DESC, event_id;
