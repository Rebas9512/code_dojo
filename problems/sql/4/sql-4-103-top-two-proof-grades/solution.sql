WITH ranked AS (
    SELECT sheet, rack, DENSE_RANK() OVER (PARTITION BY rack ORDER BY score DESC) AS tier
    FROM proof_marks WHERE score IS NOT NULL
)
SELECT rack, sheet FROM ranked WHERE tier <= 2;
