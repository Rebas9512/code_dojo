SELECT slip, COALESCE(LAG(reading) OVER (PARTITION BY press ORDER BY day NULLS LAST, slip), 0) AS previous
FROM press_readings;
