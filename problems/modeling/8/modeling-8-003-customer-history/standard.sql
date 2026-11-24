CREATE TABLE dim_customer (
    customer_key integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_code text NOT NULL,
    tier text NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    UNIQUE (customer_code, valid_from)
);

INSERT INTO dim_customer (customer_code, tier, valid_from, valid_to)
SELECT customer_code, tier, valid_from,
       LEAD(valid_from) OVER (PARTITION BY customer_code ORDER BY valid_from)
FROM warehouse_feed.customers
WHERE batch_no = 1;
