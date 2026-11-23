SELECT sheet, RANK() OVER (PARTITION BY rack ORDER BY score DESC NULLS LAST) AS place
FROM proof_marks;
