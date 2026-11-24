WITH eligible AS (
    SELECT r.joined_on,
           EXISTS (
               SELECT 1
               FROM logins l
               WHERE l.user_id = r.user_id
                 AND l.logged_at::date = r.joined_on + 1
           ) AS returned
    FROM readers r
    WHERE r.joined_on + 1 <= DATE '2025-03-14'
), counts AS (
    SELECT joined_on, COUNT(*) AS readers_n, COUNT(*) FILTER (WHERE returned) AS returned_n
    FROM eligible
    GROUP BY joined_on
)
SELECT joined_on, readers_n, returned_n, ROUND(returned_n::numeric / readers_n, 4) AS rate
FROM counts
ORDER BY joined_on;
