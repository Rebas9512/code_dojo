CREATE TABLE products (product_id integer PRIMARY KEY, label text NOT NULL);
CREATE TABLE requests (product_id integer REFERENCES products, ordered_on date NOT NULL, units integer NOT NULL);
INSERT INTO products VALUES (1,'夜航'),(2,'早春');
INSERT INTO requests VALUES (1,'2025-04-01',40),(1,'2025-04-30',60),(2,'2025-05-01',120),(2,'2025-04-28',20);
