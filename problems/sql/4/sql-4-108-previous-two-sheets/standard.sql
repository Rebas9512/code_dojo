SELECT slip, SUM(reading) OVER (
    PARTITION BY press
    ORDER BY day NULLS LAST, slip
    ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING
) AS prior_total
FROM press_readings;
