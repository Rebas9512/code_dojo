WITH first_orders AS (
    SELECT user_id, ____ AS first_day FROM orders GROUP BY user_id
)
SELECT first_day, COUNT(*) AS buyers FROM first_orders GROUP BY first_day;
