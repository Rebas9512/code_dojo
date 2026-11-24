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
), counts AS (
    SELECT arm, COUNT(*) AS n, COUNT(*) FILTER (WHERE converted) AS x
    FROM outcomes
    GROUP BY arm
), paired AS (
    SELECT b.x::numeric / b.n - a.x::numeric / a.n AS rate_diff,
           (a.x + b.x)::numeric / (a.n + b.n) AS pooled,
           1.0 / a.n + 1.0 / b.n AS inverse_sizes
    FROM counts a
    JOIN counts b ON a.arm = 'A' AND b.arm = 'B'
)
SELECT ROUND(rate_diff / NULLIF(SQRT(pooled * (1 - pooled) * inverse_sizes), 0), 4) AS z
FROM paired;
