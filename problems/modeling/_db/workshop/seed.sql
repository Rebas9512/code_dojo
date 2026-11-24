-- 首批销售明细、客户等级和开店时的商品目录。
INSERT INTO warehouse_feed.sales VALUES
    (1, 101, '2025-01-31', 'C01', 'P01', 2),
    (1, 102, '2025-02-01', 'C01', 'P02', 1),
    (1, 103, '2025-02-15', 'C02', 'P01', 4),
    (1, 104, '2025-02-28', 'C02', 'P03', 0);

INSERT INTO warehouse_feed.customers VALUES
    (1, 'C01', '2025-02-01', 'silver'),
    (1, 'C02', '2025-01-01', 'base'),
    (1, 'C01', '2025-01-01', 'base');

INSERT INTO warehouse_feed.catalog VALUES
    ('P01', 'Notebook'), ('P02', 'Pencil'), ('P03', 'Notebook'), ('P04', 'Ruler');
