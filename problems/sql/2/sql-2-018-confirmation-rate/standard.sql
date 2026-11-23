SELECT a.account_id,
       ROUND(AVG(CASE WHEN c.outcome = 'ok' THEN 1 ELSE 0 END), 2) AS confirmation_rate
FROM accounts a
LEFT JOIN checks c ON c.account_id = a.account_id
GROUP BY a.account_id;
