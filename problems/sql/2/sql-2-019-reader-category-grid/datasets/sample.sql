CREATE VIEW categories AS SELECT DISTINCT category FROM books;
CREATE VIEW purchases AS
SELECT o.user_id, b.category, o.order_id
FROM orders o JOIN order_items i ON i.order_id = o.order_id
JOIN books b ON b.book_id = i.book_id WHERE o.status <> 'cancelled';
