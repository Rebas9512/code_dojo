WITH per_reader AS (
    SELECT r.user_id, channel AS segment, COALESCE(SUM(p.amount), 0) AS net
    FROM readers r LEFT JOIN payments p ON p.user_id=r.user_id
      AND p.paid_at::date >= r.joined_on AND p.paid_at::date ____
    WHERE r.joined_on + 7-1 <= DATE '2025-03-14' GROUP BY r.user_id
)
SELECT segment AS channel, ROUND(AVG(net), 2) AS ltv FROM per_reader GROUP BY segment ORDER BY segment;
