CREATE TABLE catalog (sku int PRIMARY KEY);
INSERT INTO catalog VALUES
    (10),
    (20),
    (30);
CREATE TABLE receipts (customer int, sku int REFERENCES catalog);
INSERT INTO receipts VALUES
    (1, 10),
    (1, 20),
    (1, 30),
    (2, 10),
    (2, 10),
    (2, 30);
