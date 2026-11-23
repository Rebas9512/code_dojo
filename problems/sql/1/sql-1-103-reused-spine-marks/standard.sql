SELECT mark
FROM spine_log
GROUP BY mark
HAVING COUNT(*) > 1;
