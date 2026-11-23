WITH calendar AS (
    SELECT first_day + n AS day
    FROM display_period,
         generate_series(0, last_day - first_day) AS offsets(n)
)
SELECT c.day, COUNT(t.ticket) AS tickets
FROM calendar c
LEFT JOIN show_tickets t ON t.day = c.day
GROUP BY c.day
ORDER BY c.day;
