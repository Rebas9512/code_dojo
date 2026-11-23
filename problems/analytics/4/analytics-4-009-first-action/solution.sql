WITH ranked AS (
    SELECT e.*, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY happened_at ASC, event_id ASC) AS n
    FROM events e
)
SELECT user_id, event_id, action FROM ranked WHERE n=1 ORDER BY user_id;
