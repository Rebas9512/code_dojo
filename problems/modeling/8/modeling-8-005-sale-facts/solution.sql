CREATE TABLE fact_sale (
    line_id integer PRIMARY KEY,
    sold_on date NOT NULL,
    customer_key integer NOT NULL REFERENCES dim_customer (customer_key),
    product_key integer NOT NULL REFERENCES dim_product (product_key),
    qty integer NOT NULL
);

CREATE VIEW keyed_sale AS
SELECT r.batch_no, r.line_id, r.sold_on, c.customer_key, p.product_key, r.qty
FROM raw_sale r
JOIN dim_customer c ON c.customer_code = r.customer_code
                   AND c.valid_from <= r.sold_on
                   AND (c.valid_to IS NULL OR r.sold_on < c.valid_to)
JOIN dim_product p ON p.sku = r.sku;

INSERT INTO fact_sale (line_id, sold_on, customer_key, product_key, qty)
SELECT line_id, sold_on, customer_key, product_key, qty
FROM keyed_sale
WHERE batch_no = 1;
