CREATE TABLE stock_checks (book_id integer NOT NULL REFERENCES books, sold integer NOT NULL, returned integer NOT NULL);
INSERT INTO stock_checks VALUES (3,4,1),(3,6,1),(14,0,0);
