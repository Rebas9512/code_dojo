-- 七月只有无效订单。八月只有空订单，九月只有匿名作者的销售。
INSERT INTO orders (order_id, user_id, order_date, status, coupon_code) VALUES
    (301, 17, '2025-07-01', 'paid', 'TEST'),
    (302, 17, '2025-07-31', 'cancelled', NULL),
    (303, 17, '2025-08-31', 'paid', NULL),
    (304, 18, '2025-09-01', 'delivered', 'CONTEST');

INSERT INTO order_items (order_id, book_id, quantity, unit_price) VALUES
    (301, 7, 1, 14.00), (302, 7, 1, 14.00), (304, 25, 2, 8.50);
