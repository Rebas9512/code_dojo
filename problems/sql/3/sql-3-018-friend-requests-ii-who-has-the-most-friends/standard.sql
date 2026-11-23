WITH endpoints AS (
    SELECT sender AS id
    FROM friendships
    UNION ALL
    SELECT receiver
    FROM friendships
)
SELECT id, COUNT(*) AS friends
FROM endpoints
GROUP BY id
ORDER BY friends DESC
LIMIT 1;
