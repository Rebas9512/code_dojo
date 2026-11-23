CREATE VIEW city_kpi AS
SELECT d.city,COUNT(DISTINCT p.order_id) AS orders_n,SUM(p.units) AS units_n
FROM parcels p JOIN depots d ON p.depot_id=d.id GROUP BY d.city;
