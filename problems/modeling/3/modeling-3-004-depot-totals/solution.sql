INSERT INTO daily SELECT depot,SUM(qty) FROM scans GROUP BY depot;
