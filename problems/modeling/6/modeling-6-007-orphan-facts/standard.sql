SELECT f.event_id
FROM facts f
LEFT JOIN depots d ON d.id = f.depot_id
WHERE f.depot_id IS NOT NULL AND d.id IS NULL;
