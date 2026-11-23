-- 只剩 5 本书（先删掉引用它们的评分和订单明细）
DELETE FROM ratings;
DELETE FROM order_items;
DELETE FROM books WHERE book_id > 5;
