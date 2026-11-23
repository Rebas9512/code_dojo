CREATE VIEW book_purchases AS SELECT o.user_id, b.category, i.quantity FROM orders o JOIN order_items i USING(order_id) JOIN books b USING(book_id) WHERE o.status <> 'cancelled';
