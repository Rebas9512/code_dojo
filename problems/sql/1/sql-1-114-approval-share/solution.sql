SELECT desk, ROUND(1.0 * COUNT(*) FILTER (WHERE pass = 1) / COUNT(*), 2) AS share
FROM proof_votes GROUP BY desk;
