WITH first_views AS (
    SELECT user_id, MIN(happened_at) AS viewed
    FROM events
    WHERE action = 'view'
    GROUP BY user_id
), first_carts AS (
    SELECT p.user_id, MIN(e.happened_at) AS carted
    FROM first_views p
    JOIN events e
        ON e.user_id = p.user_id AND e.action = 'cart' AND e.happened_at > p.viewed
    GROUP BY p.user_id
)
SELECT c.user_id
FROM first_carts c
LEFT JOIN events e
    ON e.user_id = c.user_id AND e.action = 'order' AND e.happened_at > c.carted
WHERE e.event_id IS NULL
ORDER BY c.user_id;
