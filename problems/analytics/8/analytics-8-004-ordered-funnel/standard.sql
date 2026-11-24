CREATE VIEW order_funnel AS
WITH views AS (
    SELECT user_id, MIN(local_at) AS viewed_at
    FROM clean_activity
    WHERE action = 'view'
    GROUP BY user_id
), carts AS (
    SELECT v.user_id, MIN(e.local_at) AS carted_at
    FROM views v
    LEFT JOIN clean_activity e ON e.user_id = v.user_id
        AND e.action = 'cart' AND e.local_at > v.viewed_at
    GROUP BY v.user_id
), orders AS (
    SELECT c.user_id, c.carted_at, MIN(e.local_at) AS ordered_at
    FROM carts c
    LEFT JOIN clean_activity e ON e.user_id = c.user_id
        AND e.action = 'order' AND e.local_at > c.carted_at
    GROUP BY c.user_id, c.carted_at
)
SELECT COUNT(*) AS viewers, COUNT(carted_at) AS carters, COUNT(ordered_at) AS buyers,
       ROUND(COUNT(ordered_at)::numeric / NULLIF(COUNT(*), 0), 4) AS order_rate
FROM orders;
