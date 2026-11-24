SELECT order_month, COUNT(DISTINCT user_id) AS repeat_count
FROM (
    SELECT order_month, user_id,
           ROW_NUMBER() OVER (
               PARTITION BY user_id
               ORDER BY order_date, order_id
           ) AS purchase_no
    FROM valid_orders
) AS purchases
WHERE purchase_no > 1
GROUP BY order_month
