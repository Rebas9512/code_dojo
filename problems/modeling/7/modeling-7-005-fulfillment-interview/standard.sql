CREATE TABLE depots (
    id int PRIMARY KEY,
    city text
);

CREATE TABLE parcels (
    id int PRIMARY KEY,
    order_id int,
    depot_id int REFERENCES depots(id),
    shipped_on date,
    units int
);

INSERT INTO depots (id, city)
SELECT DISTINCT depot_id, city
FROM dispatch;

INSERT INTO parcels (id, order_id, depot_id, shipped_on, units)
SELECT parcel_id, order_id, depot_id, shipped_on, units
FROM dispatch;

CREATE VIEW city_kpi AS
SELECT d.city, COUNT(DISTINCT p.order_id) AS orders_n, SUM(p.units) AS units_n
FROM parcels p
JOIN depots d ON d.id = p.depot_id
GROUP BY d.city;

CREATE VIEW day_kpi AS
SELECT shipped_on, COUNT(*) AS parcels_n, COUNT(DISTINCT order_id) AS orders_n
FROM parcels
GROUP BY shipped_on;

CREATE VIEW splits AS
SELECT order_id, COUNT(*) AS parcels_n
FROM parcels
GROUP BY order_id
HAVING COUNT(*) > 1;
