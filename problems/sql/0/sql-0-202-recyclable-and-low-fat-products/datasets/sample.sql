CREATE TABLE products (
    product_id integer PRIMARY KEY,
    low_fats text NOT NULL,
    recyclable text NOT NULL
);

INSERT INTO products VALUES
    (11, 'Y', 'N'),
    (26, 'Y', 'Y'),
    (30, 'N', 'Y'),
    (44, 'N', 'N');
