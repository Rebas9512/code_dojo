WITH device_counts AS (
    SELECT DATE_TRUNC('week', viewed_at)::date AS week_start, device,
           COUNT(*) FILTER (WHERE carted_at > viewed_at) AS carts,
           COUNT(*) FILTER (WHERE carted_at > viewed_at AND ordered_at > carted_at) AS orders
    FROM checkout_visits
    GROUP BY week_start, device
)
SELECT week_start, device, carts, orders,
       ROUND(orders::numeric / NULLIF(carts, 0), 4) AS cart_order
FROM device_counts
ORDER BY week_start, device;
