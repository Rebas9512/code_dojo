INSERT INTO members SELECT id,tag FROM inbox
ON CONFLICT(id) DO UPDATE SET tag=excluded.tag;
