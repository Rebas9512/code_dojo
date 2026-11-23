WITH neighbors AS (
    SELECT event, reader, at_time, LAG(at_time) OVER (PARTITION BY reader ORDER BY at_time, event) AS prev
    FROM desk_actions WHERE at_time IS NOT NULL
), numbered AS (
    SELECT event, reader, at_time,
           SUM(CASE WHEN prev IS NULL OR at_time - prev > INTERVAL '30 minutes' THEN 1 ELSE 0 END)
           OVER (PARTITION BY reader ORDER BY at_time, event ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS session_no
    FROM neighbors
)
SELECT reader, MAX(session_no) AS sessions FROM numbered GROUP BY reader;
