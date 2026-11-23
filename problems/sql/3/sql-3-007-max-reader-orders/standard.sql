SELECT MAX(order_count) AS most_orders
FROM (
    SELECT COUNT(*) AS order_count
    FROM orders
    GROUP BY user_id
) AS orders_per_reader;
