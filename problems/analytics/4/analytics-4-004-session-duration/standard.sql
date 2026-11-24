WITH neighbors AS (
    SELECT user_id, event_id, happened_at,
           LAG(happened_at) OVER (PARTITION BY user_id ORDER BY happened_at, event_id) AS prev_at
    FROM events
), starts AS (
    SELECT user_id, event_id, happened_at,
           CASE WHEN prev_at IS NULL OR happened_at - prev_at >= INTERVAL '30 minutes'
                THEN 1 ELSE 0 END AS is_start
    FROM neighbors
), sessions AS (
    SELECT user_id, happened_at,
           SUM(is_start) OVER (PARTITION BY user_id ORDER BY happened_at, event_id) AS session_no
    FROM starts
)
SELECT user_id, session_no,
       ROUND(EXTRACT(EPOCH FROM MAX(happened_at) - MIN(happened_at)) / 60, 2) AS minutes
FROM sessions
GROUP BY user_id, session_no
ORDER BY user_id, session_no;
