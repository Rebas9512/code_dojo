WITH ranked AS (
    SELECT route, delay_days, ROW_NUMBER() OVER (PARTITION BY route ORDER BY delay_days NULLS LAST, shipment) AS pos,
           COUNT(delay_days) OVER (PARTITION BY route) AS n FROM shipments
)
SELECT route, MAX(n) AS measured,
       AVG(CASE WHEN 2 * pos BETWEEN n AND n + 2 THEN delay_days END) AS median_days
FROM ranked GROUP BY route;
