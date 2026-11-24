SELECT DATE_TRUNC('month', occurred_on)::date AS month_start,
       SUM(CASE WHEN kind = 'start' THEN price ELSE 0.00 END) AS added,
       SUM(CASE WHEN kind = 'renew' THEN price ELSE 0.00 END) AS renewed,
       SUM(CASE WHEN kind = 'cancel' THEN price ELSE 0.00 END) AS lost
FROM memberships
GROUP BY month_start
ORDER BY month_start;
