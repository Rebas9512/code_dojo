CREATE TABLE price_tags (book_id integer REFERENCES books, starts_on date, ends_on date NOT NULL, price numeric NOT NULL, PRIMARY KEY (book_id, starts_on));
CREATE TABLE counter_sales (sale_id integer PRIMARY KEY, book_id integer NOT NULL REFERENCES books, sold_on date NOT NULL);
INSERT INTO price_tags VALUES (3,'2025-01-01','2025-01-31',40),(3,'2025-02-01','2025-02-28',45),(6,'2025-01-01','2025-01-31',20);
INSERT INTO counter_sales VALUES (1,3,'2025-01-31'),(2,3,'2025-02-01'),(3,6,'2025-03-01');
