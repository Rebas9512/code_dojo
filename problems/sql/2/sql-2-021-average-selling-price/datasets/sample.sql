CREATE TABLE prices (product_id integer, first_day date, last_day date NOT NULL, price numeric NOT NULL, PRIMARY KEY (product_id, first_day));
CREATE TABLE unit_sales (product_id integer NOT NULL, sold_on date NOT NULL, units integer NOT NULL);
INSERT INTO prices VALUES (2,'2025-01-01','2025-01-15',10),(2,'2025-01-16','2025-01-31',20),(3,'2025-01-01','2025-01-31',12);
INSERT INTO unit_sales VALUES (2,'2025-01-15',1),(2,'2025-01-16',2);
