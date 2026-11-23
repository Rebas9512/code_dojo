WITH clean AS (
    SELECT user_id, MIN(arm) AS arm, MIN(assigned_at) AS entered FROM assignments
    WHERE experiment='cover' GROUP BY user_id HAVING COUNT(DISTINCT arm)=1
), plan(arm, target) AS (VALUES ('A', 0.60), ('B', 0.40)), sizes AS (
    SELECT p.arm, p.target, COUNT(c.user_id) AS observed FROM plan p LEFT JOIN clean c ON c.arm=p.arm
    GROUP BY p.arm, p.target
), expected AS (
    SELECT arm, observed, SUM(observed) OVER () * target AS expected_n FROM sizes
)
SELECT arm, observed, ROUND(expected_n, 2) AS expected_n FROM expected ORDER BY arm;
