WITH ranked AS (
    SELECT user_id,
           event_id,
           action,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY happened_at DESC, event_id DESC) AS position
    FROM events
)
SELECT user_id, event_id, action
FROM ranked
WHERE position = 1
ORDER BY user_id;
