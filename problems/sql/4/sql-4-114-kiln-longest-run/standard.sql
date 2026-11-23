WITH days AS (
    SELECT DISTINCT kiln, day
    FROM kiln_checks
    WHERE day IS NOT NULL
), tagged AS (
    SELECT kiln, day, day - (ROW_NUMBER() OVER (PARTITION BY kiln ORDER BY day))::int AS block
    FROM days
), lengths AS (
    SELECT kiln, COUNT(*) AS length
    FROM tagged
    GROUP BY kiln, block
)
SELECT kiln, MAX(length) AS longest
FROM lengths
GROUP BY kiln;
