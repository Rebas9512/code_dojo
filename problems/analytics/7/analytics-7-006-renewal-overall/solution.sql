WITH weekly AS (
    SELECT DATE_TRUNC('week', due_on)::date AS week_start,
           COUNT(*) AS due_n, COUNT(*) FILTER (WHERE renewed_on BETWEEN due_on AND due_on+6) AS renewed_n
    FROM renewal_offers GROUP BY week_start
)
SELECT week_start, due_n, renewed_n, ROUND(renewed_n::numeric/due_n, 4) AS rate
FROM weekly ORDER BY week_start;
