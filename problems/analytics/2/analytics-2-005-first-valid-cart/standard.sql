WITH first_views AS (
    SELECT user_id, MIN(happened_at) AS viewed
    FROM events
    WHERE action = 'view'
    GROUP BY user_id
)
SELECT p.user_id, p.viewed, MIN(e.happened_at) AS carted
FROM first_views p
LEFT JOIN events e
    ON e.user_id = p.user_id AND e.action = 'cart' AND e.happened_at > p.viewed
GROUP BY p.user_id, p.viewed
ORDER BY p.user_id;
