WITH changes AS (SELECT id,SUM(n) AS delta FROM entries GROUP BY id)
INSERT INTO purse SELECT id,delta FROM changes ON CONFLICT(id) DO UPDATE SET n=purse.n+excluded.n;
