CREATE TABLE goods (goods_id integer PRIMARY KEY, label text NOT NULL);
CREATE TABLE sales (sale_id integer PRIMARY KEY, goods_id integer NOT NULL REFERENCES goods, sale_year integer NOT NULL, price numeric NOT NULL);
INSERT INTO goods VALUES (3,'墨盒'),(9,'笔洗'),(11,'卷轴');
INSERT INTO sales VALUES (11,3,2025,16),(12,9,2026,9);
