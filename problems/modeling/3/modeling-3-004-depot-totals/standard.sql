INSERT INTO daily (depot, units)
SELECT depot, SUM(qty)
FROM scans
GROUP BY depot;
