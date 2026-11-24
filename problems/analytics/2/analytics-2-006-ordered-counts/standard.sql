WITH first_views AS (
    SELECT user_id, MIN(happened_at) AS viewed
    FROM events
    WHERE action = 'view'
    GROUP BY user_id
), first_carts AS (
    SELECT p.user_id, MIN(e.happened_at) AS carted
    FROM first_views p
    LEFT JOIN events e
        ON e.user_id = p.user_id AND e.action = 'cart' AND e.happened_at > p.viewed
    GROUP BY p.user_id
), first_orders AS (
    SELECT p.user_id, p.carted, MIN(e.happened_at) AS ordered_at
    FROM first_carts p
    LEFT JOIN events e
        ON e.user_id = p.user_id AND e.action = 'order' AND e.happened_at > p.carted
    GROUP BY p.user_id, p.carted
)
SELECT COUNT(*) AS viewers, COUNT(carted) AS carts, COUNT(ordered_at) AS orders
FROM first_orders;
