-- 销售可能早于首个客户版本，或引用未登记的商品；数量也可能无效。
INSERT INTO warehouse_feed.catalog VALUES ('P09', 'Ruler');
INSERT INTO warehouse_feed.customers VALUES (1, 'C09', '2025-02-01', 'base');
INSERT INTO warehouse_feed.sales VALUES
    (1, 301, '2025-01-31', 'C09', 'P09', 1),
    (1, 302, '2025-02-01', 'C09', 'X', 2),
    (1, 303, '2025-02-01', 'C09', 'P09', -1),
    (2, 304, '2025-03-01', 'unknown', 'X', 1),
    (2, 305, '2025-03-01', 'C09', 'P09', 0);
