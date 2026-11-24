INSERT INTO members (id, tag)
SELECT id, tag
FROM inbox
ON CONFLICT (id) DO NOTHING;
