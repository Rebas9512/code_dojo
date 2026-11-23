SELECT slip, AVG(reading) OVER (
    PARTITION BY press
    ORDER BY day NULLS LAST, slip
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
) AS rolling_mean
FROM press_readings;
