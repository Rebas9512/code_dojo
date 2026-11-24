SELECT DATE_TRUNC('month', occurred_on)::date AS month_start,
       SUM(CASE kind WHEN 'start' THEN price WHEN 'cancel' THEN -price ELSE 0.00 END) AS net_mrr
FROM memberships
GROUP BY month_start
ORDER BY month_start;
