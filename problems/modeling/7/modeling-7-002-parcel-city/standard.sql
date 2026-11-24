CREATE VIEW city_kpi AS
SELECT d.city, COUNT(DISTINCT p.order_id) AS orders_n, SUM(p.units) AS units_n
FROM parcels p
JOIN depots d ON d.id = p.depot_id
GROUP BY d.city;
