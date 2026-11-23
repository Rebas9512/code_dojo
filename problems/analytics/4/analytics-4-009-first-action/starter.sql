WITH ranked AS (
    SELECT e.*, ROW_NUMBER() OVER (____ ORDER BY happened_at ASC, event_id ASC) AS n
    FROM events e
)
SELECT user_id, event_id, action FROM ranked WHERE n=1 ORDER BY user_id;
