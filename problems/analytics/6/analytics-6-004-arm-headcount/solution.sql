WITH clean AS (
    SELECT user_id, MIN(arm) AS arm, MIN(assigned_at) AS entered FROM assignments
    WHERE experiment='cover' GROUP BY user_id HAVING COUNT(DISTINCT arm)=1
)
SELECT arm, COUNT(*) AS readers_n FROM clean GROUP BY arm ORDER BY arm;
