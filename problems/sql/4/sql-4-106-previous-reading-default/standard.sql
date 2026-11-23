SELECT slip, LAG(reading, 1, 0) OVER (PARTITION BY press ORDER BY day NULLS LAST, slip) AS previous
FROM press_readings;
