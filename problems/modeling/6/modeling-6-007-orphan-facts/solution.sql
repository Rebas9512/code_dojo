SELECT f.event_id FROM facts f LEFT JOIN depots d ON f.depot_id=d.id WHERE d.id IS NULL AND f.depot_id IS NOT NULL;
