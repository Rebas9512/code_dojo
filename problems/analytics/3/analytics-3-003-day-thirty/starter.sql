WITH eligible AS (
    SELECT r.*, EXISTS (
        SELECT 1 FROM logins l WHERE l.user_id = r.user_id
          AND l.logged_at::date >= r.joined_on + 30 AND l.logged_at::date <= DATE '2025-03-14'
    ) AS returned FROM readers r WHERE r.joined_on + 30 <= DATE '2025-03-14'
)
SELECT device, COUNT(*) AS readers_n, COUNT(*) FILTER (WHERE returned) AS returned_n,
       ROUND(COUNT(*) FILTER (WHERE returned)::numeric / COUNT(*), 4) AS rate
FROM eligible GROUP BY device ORDER BY device;
