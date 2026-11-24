-- 连续版本、同名商品，以及更正时发生变化的日期和两个维度键。
INSERT INTO warehouse_feed.customers VALUES
    (1, 'C07', '2025-02-10', 'gold'),
    (1, 'C07', '2025-01-05', 'silver'),
    (2, 'C07', '2025-03-15', 'silver');
INSERT INTO warehouse_feed.catalog VALUES ('007', 'Pencil');
INSERT INTO warehouse_feed.sales VALUES
    (1, 201, '2025-01-05', 'C07', '007', 1),
    (1, 202, '2025-02-09', 'C07', '007', 2),
    (1, 203, '2025-02-10', 'C07', '007', 3),
    (2, 201, '2025-03-15', 'C01', 'P02', 1),
    (2, 204, '2025-03-15', 'C07', '007', 4);
