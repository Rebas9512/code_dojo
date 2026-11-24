CREATE VIEW app_sessions AS
WITH neighbors AS (
    SELECT user_id, local_at, source_id,
           LAG(local_at) OVER (PARTITION BY user_id ORDER BY local_at, source_id) AS prev_at
    FROM clean_activity
    WHERE action <> 'login'
), starts AS (
    SELECT user_id, local_at, source_id,
           CASE WHEN prev_at IS NULL OR local_at - prev_at >= INTERVAL '30 minutes'
                THEN 1 ELSE 0 END AS starts_here
    FROM neighbors
), numbered AS (
    SELECT user_id, local_at,
           SUM(starts_here) OVER (PARTITION BY user_id ORDER BY local_at, source_id) AS session_no
    FROM starts
)
SELECT user_id, session_no, MIN(local_at) AS started_at,
       MAX(local_at) AS ended_at, COUNT(*) AS event_count
FROM numbered
GROUP BY user_id, session_no;
