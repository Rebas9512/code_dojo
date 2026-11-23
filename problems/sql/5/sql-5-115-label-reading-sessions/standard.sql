WITH neighbors AS (
    SELECT event, reader, at_time,
           LAG(at_time) OVER (PARTITION BY reader ORDER BY at_time, event) AS previous_time
    FROM desk_actions
    WHERE at_time IS NOT NULL
)
SELECT event,
       SUM(CASE WHEN previous_time IS NULL OR at_time - previous_time > INTERVAL '30 minutes'
                THEN 1 ELSE 0 END) OVER (
           PARTITION BY reader ORDER BY at_time, event
           ROWS UNBOUNDED PRECEDING
       ) AS session_no
FROM neighbors;
