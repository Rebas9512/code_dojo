WITH RECURSIVE tree AS (
    SELECT user_id, 0 AS depth
    FROM users
    WHERE referrer_id IS NULL
    UNION ALL
    SELECT child.user_id, parent.depth + 1
    FROM tree parent
    JOIN users child ON child.referrer_id = parent.user_id
)
SELECT user_id, depth
FROM tree;
