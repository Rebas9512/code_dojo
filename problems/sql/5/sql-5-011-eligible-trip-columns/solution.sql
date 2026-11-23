WITH eligible AS (
    SELECT t.day, t.status FROM trips t JOIN accounts r ON r.id = t.rider
    JOIN accounts d ON d.id = t.driver WHERE r.blocked = false AND d.blocked = false
)
SELECT day, COUNT(CASE WHEN status = 'done' THEN 1 END) AS done,
       COUNT(CASE WHEN status = 'rider_cancel' THEN 1 END) AS rider_cancel,
       COUNT(CASE WHEN status = 'driver_cancel' THEN 1 END) AS driver_cancel,
       1.0 * COUNT(CASE WHEN status <> 'done' THEN 1 END) / COUNT(*) AS cancel_rate
FROM eligible GROUP BY day;
