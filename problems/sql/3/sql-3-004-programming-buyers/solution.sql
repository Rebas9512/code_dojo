SELECT user_id, name FROM users
WHERE user_id IN (
    SELECT o.user_id FROM orders o
    JOIN order_items i ON i.order_id = o.order_id
    JOIN books b ON b.book_id = i.book_id
    WHERE b.category = 'programming' AND o.status <> 'cancelled'
);
