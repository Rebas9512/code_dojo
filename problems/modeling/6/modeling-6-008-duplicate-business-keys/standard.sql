SELECT code, COUNT(*)
FROM intake
GROUP BY code
HAVING COUNT(*) > 1;
