-- 同名作者各自结算。两类并列第一，下一类排第二。三笔同日订单属于同一位新读者。
UPDATE authors SET name = 'Lin Qiu' WHERE author_id = 3;

INSERT INTO orders (order_id, user_id, order_date, status, coupon_code) VALUES
    (403, 18, '2025-07-31', 'paid', 'TESTING'),
    (402, 18, '2025-07-31', 'shipped', NULL),
    (401, 18, '2025-07-31', 'delivered', NULL);

INSERT INTO order_items (order_id, book_id, quantity, unit_price) VALUES
    (401, 1, 1, 10.00), (401, 9, 1, 10.00),
    (402, 7, 2, 10.00), (403, 6, 1, 5.00);
