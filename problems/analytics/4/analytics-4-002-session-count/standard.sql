WITH neighbors AS (
    SELECT user_id, event_id, happened_at,
           LAG(happened_at) OVER (PARTITION BY user_id ORDER BY happened_at, event_id) AS prev_at
    FROM events
), starts AS (
    SELECT user_id,
           CASE WHEN prev_at IS NULL OR happened_at - prev_at >= INTERVAL '30 minutes'
                THEN 1 ELSE 0 END AS is_start
    FROM neighbors
)
SELECT user_id, SUM(is_start) AS sessions
FROM starts
GROUP BY user_id
ORDER BY user_id;
