SELECT user_id, MIN(arm) AS arm
FROM assignments
WHERE experiment = 'cover'
GROUP BY user_id
HAVING COUNT(DISTINCT arm) = 1
ORDER BY user_id;
