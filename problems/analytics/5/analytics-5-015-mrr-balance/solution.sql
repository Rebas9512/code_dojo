WITH monthly AS (
    SELECT DATE_TRUNC('month', occurred_on)::date AS month_start,
           SUM(CASE WHEN kind='start' THEN price ELSE 0 END) AS added,
           SUM(CASE WHEN kind='renew' THEN price ELSE 0 END) AS renewed,
           SUM(CASE WHEN kind='cancel' THEN price ELSE 0 END) AS lost
    FROM memberships GROUP BY month_start
)
SELECT month_start, ROUND(SUM(added-lost) OVER (ORDER BY month_start), 2) AS closing_mrr FROM monthly ORDER BY month_start;
