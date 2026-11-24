-- 题面里的单行小账本。一名客户、一种商品、一笔销售，次批没有来料。
DELETE FROM warehouse_feed.sales;
DELETE FROM warehouse_feed.customers;
DELETE FROM warehouse_feed.catalog;
INSERT INTO warehouse_feed.catalog VALUES ('B7', 'Pen');
INSERT INTO warehouse_feed.customers VALUES (1, 'Solo', '2025-01-01', 'base');
INSERT INTO warehouse_feed.sales VALUES (1, 7, '2025-01-01', 'Solo', 'B7', 1);
