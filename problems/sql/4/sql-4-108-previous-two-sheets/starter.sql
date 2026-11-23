SELECT slip, SUM(reading) OVER (
    PARTITION BY press ORDER BY day NULLS LAST, slip
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
) AS prior_total FROM press_readings;
