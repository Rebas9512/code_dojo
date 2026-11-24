WITH eligible AS (
    SELECT r.channel,
           EXISTS (
               SELECT 1
               FROM logins l
               WHERE l.user_id = r.user_id
                 AND l.logged_at::date = r.joined_on + 7
           ) AS returned
    FROM readers r
    WHERE r.joined_on + 7 <= DATE '2025-03-14'
), counts AS (
    SELECT channel, COUNT(*) AS readers_n, COUNT(*) FILTER (WHERE returned) AS returned_n
    FROM eligible
    GROUP BY channel
)
SELECT channel, readers_n, returned_n, ROUND(returned_n::numeric / readers_n, 4) AS rate
FROM counts
ORDER BY channel;
