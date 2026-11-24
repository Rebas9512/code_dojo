WITH channel_sizes AS (
    SELECT channel, COUNT(*) AS n
    FROM readers
    GROUP BY channel
)
SELECT channel, n, ROUND(n / SUM(n) OVER (), 4) AS share
FROM channel_sizes
ORDER BY channel;
