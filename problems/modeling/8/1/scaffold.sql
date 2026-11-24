-- 小数仓：在 workshop 项目库中按顺序执行。
-- @part modeling-8-001-raw-sales

-- @part modeling-8-002-load-sales

-- @part modeling-8-003-customer-history

-- @part modeling-8-004-product-catalog

-- @part modeling-8-005-sale-facts

-- 第二批到货：客户升档、等级重报、新客户，以及更正和迟到的销售明细。
INSERT INTO warehouse_feed.customers VALUES
    (2, 'C01', '2025-03-01', 'gold'),
    (2, 'C02', '2025-03-01', 'base'),
    (2, 'C03', '2025-03-01', 'base');

INSERT INTO warehouse_feed.sales VALUES
    (2, 102, '2025-02-01', 'C01', 'P02', 3),
    (2, 105, '2025-03-01', 'C01', 'P03', 5),
    (2, 106, '2025-02-28', 'C01', 'P01', 1),
    (2, 107, '2025-03-02', 'C03', 'P02', 2),
    (2, 108, '2025-03-02', 'C03', 'P02', NULL);

-- @part modeling-8-006-merge-delivery

-- @part modeling-8-007-audit-sales

-- @part modeling-8-008-close-books
