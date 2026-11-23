WITH ranked AS (
    SELECT route, delay_days,
           ROW_NUMBER() OVER (PARTITION BY route ORDER BY delay_days NULLS LAST, shipment) AS pos,
           COUNT(delay_days) OVER (PARTITION BY route) AS measured
    FROM shipments
)
SELECT route, measured,
       AVG(delay_days) FILTER (WHERE pos BETWEEN (measured + 1) / 2 AND (measured + 2) / 2) AS median_days
FROM ranked
GROUP BY route, measured;
