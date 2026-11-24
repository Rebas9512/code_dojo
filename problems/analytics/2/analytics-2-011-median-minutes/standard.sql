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
)
SELECT ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP
             (ORDER BY EXTRACT(EPOCH FROM ordered_at - viewed) / 60)::numeric, 2) AS median_minutes
FROM first_orders
WHERE ordered_at <= viewed + INTERVAL '24 hours';
