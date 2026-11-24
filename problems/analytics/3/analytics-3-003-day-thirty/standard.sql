WITH eligible AS (
    SELECT r.device,
           EXISTS (
               SELECT 1
               FROM logins l
               WHERE l.user_id = r.user_id
                 AND l.logged_at::date = r.joined_on + 30
           ) AS returned
    FROM readers r
    WHERE r.joined_on + 30 <= DATE '2025-03-14'
), counts AS (
    SELECT device, COUNT(*) AS readers_n, COUNT(*) FILTER (WHERE returned) AS returned_n
    FROM eligible
    GROUP BY device
)
SELECT device, readers_n, returned_n, ROUND(returned_n::numeric / readers_n, 4) AS rate
FROM counts
ORDER BY device;
