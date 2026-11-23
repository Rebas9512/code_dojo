CREATE TABLE visits (visit_id integer PRIMARY KEY, reader_id integer NOT NULL);
CREATE TABLE bills (bill_id integer PRIMARY KEY, visit_id integer NOT NULL REFERENCES visits);
INSERT INTO visits VALUES (1,7),(2,7),(3,9),(4,3);
INSERT INTO bills VALUES (101,2),(102,2),(103,3);
