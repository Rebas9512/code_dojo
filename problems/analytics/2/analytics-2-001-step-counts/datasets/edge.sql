DELETE FROM events WHERE user_id IN (5, 8);
INSERT INTO events VALUES
    (9001, 5, 'order', '2025-02-10 10:00'), (9002, 5, 'view', '2025-02-10 11:00'),
    (9003, 5, 'cart', '2025-02-10 11:00'), (9004, 5, 'view', '2025-02-10 11:00'),
    (9005, 8, 'view', '2025-02-01 12:00'), (9006, 8, 'order', '2025-02-02 12:00'),
    (9007, 8, 'cart', '2025-02-01 13:00');
INSERT INTO readers VALUES (91, '2025-02-01', 'ad', 'York', 'web');
INSERT INTO events VALUES (9010, 91, 'view', '2025-02-01 11:00'), (9011, 91, 'order', '2025-02-01 11:15'), (9012, 91, 'cart', '2025-02-01 11:30');
