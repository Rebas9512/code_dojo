INSERT INTO purse (id, n)
SELECT id, SUM(n)
FROM entries
GROUP BY id
ON CONFLICT (id) DO UPDATE
SET n = purse.n + EXCLUDED.n;
