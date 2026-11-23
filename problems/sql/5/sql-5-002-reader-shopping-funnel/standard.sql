WITH views AS (
    SELECT user_id, MIN(happened_at) AS viewed
    FROM reader_events
    WHERE action = 'view'
    GROUP BY user_id
), carts AS (
    SELECT v.user_id, MIN(e.happened_at) AS carted
    FROM views v
    JOIN reader_events e ON e.user_id = v.user_id AND e.happened_at > v.viewed
    WHERE e.action = 'cart'
    GROUP BY v.user_id
), buyers AS (
    SELECT DISTINCT c.user_id
    FROM carts c
    JOIN reader_events e
      ON e.user_id = c.user_id AND e.happened_at > c.carted
    WHERE e.action = 'buy'
)
SELECT (SELECT COUNT(*) FROM views) AS viewers,
       (SELECT COUNT(*) FROM carts) AS cart_users,
       (SELECT COUNT(*) FROM buyers) AS buyers;
