WITH neighbors AS (
    SELECT reader, at_time,
           LAG(at_time) OVER (PARTITION BY reader ORDER BY at_time, event) AS previous_time
    FROM desk_actions
    WHERE at_time IS NOT NULL
)
SELECT reader, COUNT(*) FILTER (
           WHERE previous_time IS NULL OR at_time - previous_time > INTERVAL '30 minutes'
       ) AS sessions
FROM neighbors
GROUP BY reader;
