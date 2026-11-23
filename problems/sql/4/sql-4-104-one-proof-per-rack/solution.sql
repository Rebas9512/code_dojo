WITH picked AS (
    SELECT rack, sheet, ROW_NUMBER() OVER (PARTITION BY rack ORDER BY score DESC, sheet) AS pos
    FROM proof_marks WHERE score IS NOT NULL
)
SELECT rack, sheet FROM picked WHERE pos = 1;
