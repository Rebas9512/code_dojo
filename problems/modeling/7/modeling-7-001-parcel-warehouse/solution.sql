CREATE TABLE depots (id int PRIMARY KEY,city text);
CREATE TABLE parcels (id int PRIMARY KEY,order_id int,depot_id int REFERENCES depots(id),shipped_on date,units int);
INSERT INTO depots SELECT DISTINCT depot_id,city FROM dispatch;
INSERT INTO parcels SELECT parcel_id,order_id,depot_id,shipped_on,units FROM dispatch;
