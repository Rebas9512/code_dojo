WITH clean AS (
    SELECT user_id, MIN(arm) AS arm, MIN(assigned_at) AS entered FROM assignments
    WHERE experiment='cover' GROUP BY user_id HAVING COUNT(*)=1
)
SELECT user_id, arm, entered FROM clean ORDER BY user_id;
