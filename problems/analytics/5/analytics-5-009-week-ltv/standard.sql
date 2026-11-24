WITH per_reader AS (
    SELECT r.user_id, channel, COALESCE(SUM(p.amount), 0) AS net
    FROM readers r
    LEFT JOIN payments p
        ON p.user_id = r.user_id AND p.paid_at::date >= r.joined_on AND p.paid_at::date < r.joined_on + 7
    WHERE r.joined_on + 6 <= DATE '2025-03-14'
    GROUP BY r.user_id
)
SELECT channel, ROUND(AVG(net), 2) AS ltv
FROM per_reader
GROUP BY channel
ORDER BY channel;
