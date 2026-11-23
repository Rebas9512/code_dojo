WITH awards AS (
    SELECT sheet, rack, score, RANK() OVER (PARTITION BY rack ORDER BY score DESC) AS place
    FROM proof_marks WHERE score IS NOT NULL
)
SELECT rack, sheet, score FROM awards WHERE place = 1;
