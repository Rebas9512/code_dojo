CREATE VIEW sold_titles AS
SELECT o.order_date AS sold_on, b.title
FROM orders o JOIN order_items i ON i.order_id = o.order_id
JOIN books b ON b.book_id = i.book_id WHERE o.status <> 'cancelled';
