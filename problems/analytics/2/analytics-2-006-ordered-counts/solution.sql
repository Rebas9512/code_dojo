WITH views AS (
    SELECT user_id, MIN(happened_at) AS viewed FROM events WHERE action = 'view' GROUP BY user_id
), carts AS (
    SELECT p.*, MIN(e.happened_at) AS carted FROM views p LEFT JOIN events e
      ON e.user_id = p.user_id AND e.action = 'cart' AND e.happened_at > p.viewed
    GROUP BY p.user_id, p.viewed
), orders AS (
    SELECT p.*, MIN(e.happened_at) AS ordered_at FROM carts p LEFT JOIN events e
      ON e.user_id = p.user_id AND e.action = 'order' AND e.happened_at > p.carted
    GROUP BY p.user_id, p.viewed, p.carted
)
SELECT COUNT(*) AS viewers, COUNT(carted) AS carts, COUNT(ordered_at) AS orders FROM orders;
