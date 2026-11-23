WITH views AS (
    SELECT user_id, MIN(happened_at) AS viewed FROM events WHERE action = 'view' GROUP BY user_id
), orders AS (
    SELECT p.*, MIN(e.happened_at) AS ordered_at FROM views p LEFT JOIN events e
      ON e.user_id = p.user_id AND e.action = 'order' AND e.happened_at > p.viewed
    GROUP BY p.user_id, p.viewed
)
SELECT COUNT(*) AS buyers FROM orders WHERE ____;
