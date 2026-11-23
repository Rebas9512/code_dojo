WITH rates AS (
    SELECT press, AVG(1.0 * sheets / hours) FILTER (WHERE month <= 6) AS early_rate,
           AVG(1.0 * sheets / hours) FILTER (WHERE month > 6) AS late_rate
    FROM print_shifts
    GROUP BY press
)
SELECT press, ROUND(early_rate, 2) AS early_rate, ROUND(late_rate, 2) AS late_rate,
       ROUND(late_rate - early_rate, 2) AS gain
FROM rates
WHERE late_rate > early_rate
ORDER BY gain DESC, press;
