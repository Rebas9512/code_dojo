CREATE VIEW cover_readout AS
WITH roster AS (
    SELECT user_id, MIN(arm) AS arm, MIN(assigned_at) AS entered_at
    FROM assignments
    WHERE experiment = 'cover' AND assigned_at < TIMESTAMP '2025-03-15 16:00'
    GROUP BY user_id
    HAVING COUNT(DISTINCT arm) = 1
), people AS (
    SELECT r.user_id, r.arm, COUNT(p.payment_id) > 0 AS bought
    FROM roster r
    LEFT JOIN payments p ON p.user_id = r.user_id AND p.amount > 0
        AND p.paid_at >= r.entered_at AND p.paid_at < r.entered_at + INTERVAL '7 days'
    WHERE r.entered_at + INTERVAL '7 days' <= TIMESTAMP '2025-03-15 16:00'
    GROUP BY r.user_id, r.arm
)
SELECT arm, COUNT(*) AS enrolled, COUNT(*) FILTER (WHERE bought) AS buyers,
       ROUND(COUNT(*) FILTER (WHERE bought)::numeric / COUNT(*), 4) AS buy_rate
FROM people
GROUP BY arm;
