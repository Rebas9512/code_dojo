SELECT o.order_id, o.order_date, b.title, i.quantity
FROM orders o
JOIN order_items i ON i.order_id = o.order_id
JOIN books b ON b.book_id = i.book_id;
