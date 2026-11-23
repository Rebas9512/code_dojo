WITH measured AS (
    SELECT day, ROW_NUMBER() OVER (ORDER BY day) AS n,
           AVG(amount) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS mean_amount
    FROM shop_calendar
)
SELECT day, mean_amount FROM measured WHERE n >= 7 ORDER BY day;
