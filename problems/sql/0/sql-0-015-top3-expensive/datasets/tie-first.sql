-- 最贵的一本变成 80 元，另有三本并列 75 元
UPDATE books SET price = 75.00 WHERE book_id IN (26, 3);
UPDATE books SET price = 80.00 WHERE book_id = 1;
