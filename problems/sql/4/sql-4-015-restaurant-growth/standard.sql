WITH daily AS (
    SELECT day, SUM(amount) AS amount
    FROM checks
    GROUP BY day
), totals AS (
    SELECT day, ROW_NUMBER() OVER (ORDER BY day) AS day_number,
           SUM(amount) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS total
    FROM daily
)
SELECT day, total, total / 7 AS average
FROM totals
WHERE day_number >= 7
ORDER BY day;
