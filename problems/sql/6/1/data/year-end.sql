-- 同一个十二月出现在两个年份。跨年老客买赠书，再购买有金额的书。
INSERT INTO orders (order_id, user_id, order_date, status, coupon_code) VALUES
    (501, 16, '2025-12-31', 'delivered', NULL),
    (502, 16, '2026-01-01', 'paid', 'test'),
    (503, 20, '2026-01-31', 'paid', 'TEST'),
    (504, 16, '2026-02-01', 'shipped', NULL),
    (505, 20, '2026-02-02', 'paid', NULL);

INSERT INTO order_items (order_id, book_id, quantity, unit_price) VALUES
    (501, 18, 1, 50.00), (502, 23, 2, 0.00), (503, 18, 1, 75.00),
    (504, 18, 2, 45.00), (505, 17, 3, 12.50);
