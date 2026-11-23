WITH ranked AS (
    SELECT dept, worker, salary, RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS place
    FROM wages WHERE salary IS NOT NULL
)
SELECT dept, worker, salary FROM ranked WHERE place = 1;
