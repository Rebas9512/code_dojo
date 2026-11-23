INSERT INTO purse SELECT id,n FROM daily
ON CONFLICT(id) DO UPDATE SET n=purse.n+excluded.n;
