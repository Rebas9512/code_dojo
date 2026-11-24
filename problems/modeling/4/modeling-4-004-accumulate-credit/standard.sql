INSERT INTO purse (id, n)
SELECT id, n
FROM daily
ON CONFLICT (id) DO UPDATE
SET n = purse.n + EXCLUDED.n;
