-- 3 月第一天和最后一天各多一单；另外有别的年份的 3 月
INSERT INTO orders (order_id, user_id, order_date, status, coupon_code) VALUES
    (134, 5,  '2025-03-01', 'delivered', NULL),
    (135, 7,  '2025-03-31', 'delivered', NULL),
    (136, 1,  '2024-03-15', 'delivered', NULL),
    (137, 2,  '2026-03-02', 'paid',      NULL),
    (138, 3,  '2025-02-28', 'delivered', NULL);
