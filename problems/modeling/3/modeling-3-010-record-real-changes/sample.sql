CREATE TABLE prices (sku text PRIMARY KEY,fee int); INSERT INTO prices VALUES ('A',10),('B',20);
CREATE TABLE revisions (sku text PRIMARY KEY,fee int); INSERT INTO revisions VALUES ('B',22);
CREATE TABLE audit (sku text, fee int);
