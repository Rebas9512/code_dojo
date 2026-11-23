WITH calendar AS (
    SELECT DATE '2025-02-26' + i AS day
    FROM generate_series(0, DATE '2025-03-03' - DATE '2025-02-26') AS offsets(i)
)
SELECT c.day, COUNT(o.order_id) AS orders
FROM calendar c
LEFT JOIN orders o ON o.order_date = c.day
GROUP BY c.day
ORDER BY c.day;
