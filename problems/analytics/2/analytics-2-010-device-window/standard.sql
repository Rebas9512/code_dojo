WITH first_views AS (
    SELECT user_id, MIN(happened_at) AS viewed
    FROM events
    WHERE action = 'view'
    GROUP BY user_id
), first_orders AS (
    SELECT p.user_id, p.viewed, MIN(e.happened_at) AS ordered_at
    FROM first_views p
    LEFT JOIN events e
        ON e.user_id = p.user_id AND e.action = 'order' AND e.happened_at > p.viewed
    GROUP BY p.user_id, p.viewed
), device_counts AS (
    SELECT device, COUNT(*) AS viewers,
           COUNT(*) FILTER (WHERE ordered_at <= viewed + INTERVAL '24 hours') AS buyers
    FROM first_orders
    JOIN readers USING (user_id)
    GROUP BY device
)
SELECT device, viewers, buyers, ROUND(buyers::numeric / viewers, 4) AS rate
FROM device_counts
ORDER BY device;
