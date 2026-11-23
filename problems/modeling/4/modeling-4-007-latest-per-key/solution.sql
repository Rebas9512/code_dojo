INSERT INTO catalog
SELECT DISTINCT ON (id) id,rev,tag FROM feed ORDER BY id,rev DESC
ON CONFLICT(id) DO UPDATE SET rev=excluded.rev,tag=excluded.tag;
