SELECT TO_CHAR(paid_on, 'YYYY-MM') AS bill_month, region, COUNT(*) AS transactions,
       SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_count,
       SUM(amount) AS total_amount,
       SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_amount
FROM payments
GROUP BY bill_month, region;
