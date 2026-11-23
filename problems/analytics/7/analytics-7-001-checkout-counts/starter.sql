WITH weekly AS (
    SELECT DATE_TRUNC('week', viewed_at)::date AS week_start,
           COUNT(*) AS visits,
           COUNT(*) FILTER (WHERE carted_at>viewed_at) AS carts,
           COUNT(*) FILTER (WHERE carted_at>viewed_at AND ____) AS orders
    FROM checkout_visits GROUP BY week_start
)
SELECT week_start, visits, carts, orders FROM weekly ORDER BY week_start;
