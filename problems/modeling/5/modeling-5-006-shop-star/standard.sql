CREATE TABLE shops (
    id int PRIMARY KEY,
    city text
);

CREATE TABLE sales (
    line_id int PRIMARY KEY,
    shop_id int REFERENCES shops(id),
    units int
);

INSERT INTO shops (id, city)
SELECT DISTINCT shop_id, city
FROM receipts;

INSERT INTO sales (line_id, shop_id, units)
SELECT line_id, shop_id, units
FROM receipts;
