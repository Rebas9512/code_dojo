WITH ranks AS (
    SELECT dept, worker, salary, DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS tier
    FROM wages
    WHERE salary IS NOT NULL
)
SELECT dept, worker, salary
FROM ranks
WHERE tier <= 3;
