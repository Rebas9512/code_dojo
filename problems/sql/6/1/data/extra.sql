-- 题面第二例：七月首个营业日，16 号读者分两单买书，另有一笔测试单和一笔取消单。
INSERT INTO orders (order_id, user_id, order_date, status, coupon_code) VALUES
    (201, 16, '2025-07-01', 'paid', NULL),
    (202, 16, '2025-07-01', 'shipped', 'SUMMER'),
    (203, 1,  '2025-07-01', 'paid', 'TEST'),
    (204, 2,  '2025-07-02', 'cancelled', NULL);

INSERT INTO order_items (order_id, book_id, quantity, unit_price) VALUES
    (201, 1,  2, 12.00), (201, 25, 1, 6.00),
    (202, 7,  2, 15.00),
    (203, 10, 1, 99.00), (204, 3, 1, 68.00);
