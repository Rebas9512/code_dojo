WITH clean AS (
    SELECT user_id, MIN(arm) AS arm, MIN(assigned_at) AS entered FROM assignments
    WHERE experiment='cover' GROUP BY user_id HAVING COUNT(DISTINCT arm)=1
), person AS (
    SELECT c.user_id, c.arm, BOOL_OR(p.amount>0) AS converted FROM clean c LEFT JOIN payments p
      ON p.user_id=c.user_id AND p.paid_at >= c.entered AND p.paid_at < c.entered + INTERVAL '7 days'
    GROUP BY c.user_id, c.arm
), rates AS (
    SELECT arm, COUNT(*) AS n, COUNT(*) FILTER (WHERE converted) AS x FROM person GROUP BY arm
), paired AS (
    SELECT a.x::numeric / a.n AS pa, b.x::numeric / b.n AS pb,
           (a.x+b.x)::numeric / (a.n+b.n) AS pooled, a.n AS na, b.n AS nb
    FROM rates a JOIN rates b ON a.arm='A' AND b.arm='B'
)
SELECT ROUND((pb-pa) / NULLIF(SQRT(pooled*(1-pooled)*(1.0/na+1.0/nb)), 0), 4) AS z
FROM paired;
