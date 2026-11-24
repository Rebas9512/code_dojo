SELECT o.order_id, i.book_id, o.order_month, b.category, b.author_id,
       i.quantity * i.unit_price AS line_amount
FROM valid_orders AS o
JOIN order_items AS i ON i.order_id = o.order_id
JOIN books AS b ON b.book_id = i.book_id
