WITH daily_counts AS (
    SELECT t.day,
           COUNT(*) FILTER (WHERE t.status = 'done') AS done,
           COUNT(*) FILTER (WHERE t.status = 'rider_cancel') AS rider_cancel,
           COUNT(*) FILTER (WHERE t.status = 'driver_cancel') AS driver_cancel,
           COUNT(*) AS trips
    FROM trips t
    JOIN accounts rider ON rider.id = t.rider
    JOIN accounts driver ON driver.id = t.driver
    WHERE NOT rider.blocked AND NOT driver.blocked
    GROUP BY t.day
)
SELECT day, done, rider_cancel, driver_cancel,
       1.0 * (rider_cancel + driver_cancel) / trips AS cancel_rate
FROM daily_counts;
