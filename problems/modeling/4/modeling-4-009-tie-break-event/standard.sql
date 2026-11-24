INSERT INTO catalog (id, rev, tag)
SELECT DISTINCT ON (id) id, rev, tag
FROM feed
ORDER BY id, rev DESC, event_id DESC
ON CONFLICT (id) DO UPDATE
SET rev = EXCLUDED.rev, tag = EXCLUDED.tag;
