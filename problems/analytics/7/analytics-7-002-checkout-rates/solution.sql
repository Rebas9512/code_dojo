WITH weekly AS (
    SELECT DATE_TRUNC('week', viewed_at)::date AS week_start,
           COUNT(*) AS visits,
           COUNT(*) FILTER (WHERE carted_at>viewed_at) AS carts,
           COUNT(*) FILTER (WHERE carted_at>viewed_at AND ordered_at>carted_at) AS orders
    FROM checkout_visits GROUP BY week_start
)
SELECT week_start, ROUND(carts::numeric/visits, 4) AS view_cart,
       ROUND(orders::numeric/NULLIF(carts, 0), 4) AS cart_order FROM weekly ORDER BY week_start;
