CREATE TABLE raw_sale (
    batch_no integer CHECK (batch_no IN (1, 2)),
    line_id integer,
    sold_on date NOT NULL,
    customer_code text NOT NULL,
    sku text NOT NULL,
    qty integer NOT NULL CHECK (qty > 0),
    PRIMARY KEY (batch_no, line_id)
);
