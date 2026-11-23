SELECT a.account_id,
       ROUND(COALESCE(SUM(CASE WHEN c.outcome = 'ok' THEN 1.0 ELSE 0 END)
                      / NULLIF(COUNT(c.check_id), 0), 0), 2) AS confirmation_rate
FROM accounts a
LEFT JOIN checks c ON c.account_id = a.account_id
GROUP BY a.account_id;
