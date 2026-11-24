WITH weekly AS (
    SELECT DATE_TRUNC('week', due_on)::date AS week_start, plan,
           COUNT(*) AS due_n,
           COUNT(*) FILTER (WHERE renewed_on BETWEEN due_on AND due_on + 6)::numeric / COUNT(*) AS rate
    FROM renewal_offers
    GROUP BY week_start, plan
), baseline AS (
    SELECT plan, due_n AS weight
    FROM weekly
    WHERE week_start = DATE '2025-02-17'
)
SELECT week_start, ROUND(SUM(rate * weight) / SUM(weight), 4) AS fixed_rate
FROM weekly
JOIN baseline USING (plan)
GROUP BY week_start
ORDER BY week_start;
