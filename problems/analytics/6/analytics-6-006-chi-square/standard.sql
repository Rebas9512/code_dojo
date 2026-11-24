WITH clean AS (
    SELECT user_id, MIN(arm) AS arm
    FROM assignments
    WHERE experiment = 'cover'
    GROUP BY user_id
    HAVING COUNT(DISTINCT arm) = 1
), plan(arm, target) AS (
    VALUES ('A', 0.60), ('B', 0.40)
), sizes AS (
    SELECT p.arm, p.target, COUNT(c.user_id) AS observed
    FROM plan p
    LEFT JOIN clean c ON c.arm = p.arm
    GROUP BY p.arm, p.target
), expected AS (
    SELECT arm, observed, SUM(observed) OVER () * target AS expected_n
    FROM sizes
)
SELECT ROUND(SUM(POWER(observed - expected_n, 2) / NULLIF(expected_n, 0)), 4) AS chi_square
FROM expected;
