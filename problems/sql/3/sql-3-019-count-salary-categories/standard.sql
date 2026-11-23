SELECT 'low' AS band, COUNT(*) AS accounts
FROM accounts
WHERE income < 20000
UNION ALL
SELECT 'middle', COUNT(*)
FROM accounts
WHERE income BETWEEN 20000 AND 50000
UNION ALL
SELECT 'high', COUNT(*)
FROM accounts
WHERE income > 50000;
