WITH neighbors AS (
    SELECT e.*, LAG(happened_at) OVER (PARTITION BY user_id ORDER BY happened_at, event_id) AS prev_at
    FROM events e
), starts AS (
    SELECT neighbors.*, CASE WHEN prev_at IS NULL OR happened_at - prev_at >= INTERVAL '30 minutes'
                             THEN 1 ELSE 0 END AS is_start FROM neighbors
), numbered AS (
    SELECT starts.*, SUM(is_start) OVER (PARTITION BY user_id ORDER BY happened_at, event_id) AS session_no
    FROM starts
)
SELECT user_id, session_no, ROUND(EXTRACT(EPOCH FROM MAX(happened_at)-MIN(happened_at))/60, 2) AS minutes
FROM numbered GROUP BY user_id, session_no ORDER BY user_id, session_no;
