CREATE VIEW clean_activity AS
WITH reports AS (
    SELECT event_id AS source_id, user_id, action, happened_at AS utc_at
    FROM events
    UNION ALL
    SELECT login_id, user_id, 'login', logged_at
    FROM logins
)
SELECT user_id, action, utc_at + INTERVAL '8 hours' AS local_at,
       MIN(source_id) AS source_id
FROM reports
WHERE utc_at < TIMESTAMP '2025-03-15 16:00'
GROUP BY user_id, action, utc_at;
