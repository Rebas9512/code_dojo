WITH tiers AS (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS tier
    FROM wages WHERE salary IS NOT NULL
)
SELECT MAX(salary) AS nth_salary FROM tiers WHERE tier = (SELECT n FROM settings);
