CREATE VIEW day_kpi AS
SELECT shipped_on, COUNT(*) AS parcels_n, COUNT(DISTINCT order_id) AS orders_n
FROM parcels
GROUP BY shipped_on;
