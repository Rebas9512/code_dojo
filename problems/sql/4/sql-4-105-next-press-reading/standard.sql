SELECT slip, LEAD(reading) OVER (PARTITION BY press ORDER BY day NULLS LAST, slip) AS next_value
FROM press_readings;
