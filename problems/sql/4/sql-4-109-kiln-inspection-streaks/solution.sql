WITH days AS (
    SELECT DISTINCT kiln, day FROM kiln_checks WHERE day IS NOT NULL
), tagged AS (
    SELECT kiln, day, day - (ROW_NUMBER() OVER (PARTITION BY kiln ORDER BY day))::int AS block
    FROM days
)
SELECT kiln, MIN(day) AS first_day, MAX(day) AS last_day, COUNT(*) AS days
FROM tagged GROUP BY kiln, block;
