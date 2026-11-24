WITH clean AS (
    SELECT user_id, MIN(arm) AS arm, MIN(assigned_at) AS entered
    FROM assignments
    WHERE experiment = 'cover'
    GROUP BY user_id
    HAVING COUNT(DISTINCT arm) = 1
), outcomes AS (
    SELECT c.user_id, c.arm, BOOL_OR(p.amount > 0) AS converted
    FROM clean c
    LEFT JOIN payments p
        ON p.user_id = c.user_id
       AND p.paid_at >= c.entered
       AND p.paid_at < c.entered + INTERVAL '7 days'
    GROUP BY c.user_id, c.arm
), rates AS (
    SELECT arm, COUNT(*) FILTER (WHERE converted)::numeric / COUNT(*) AS rate
    FROM outcomes
    GROUP BY arm
)
SELECT ROUND(100 * (b.rate - a.rate), 4) AS point_change
FROM rates a
JOIN rates b ON a.arm = 'A' AND b.arm = 'B';
