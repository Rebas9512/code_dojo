WITH clean AS (
    SELECT user_id, MIN(arm) AS arm
    FROM assignments
    WHERE experiment = 'cover'
    GROUP BY user_id
    HAVING COUNT(DISTINCT arm) = 1
), plan(arm) AS (
    VALUES ('A'), ('B')
), sizes AS (
    SELECT p.arm, COUNT(c.user_id) AS observed
    FROM plan p
    LEFT JOIN clean c ON c.arm = p.arm
    GROUP BY p.arm
)
SELECT arm, ROUND(observed / NULLIF(SUM(observed) OVER (), 0), 4) AS actual_share
FROM sizes
ORDER BY arm;
