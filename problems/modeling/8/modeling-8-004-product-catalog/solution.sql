CREATE TABLE dim_product (
    product_key integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sku text NOT NULL UNIQUE,
    product_name text NOT NULL
);

INSERT INTO dim_product (sku, product_name)
SELECT sku, product_name
FROM warehouse_feed.catalog;
