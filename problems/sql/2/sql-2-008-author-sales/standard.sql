SELECT a.author_id,
       SUM(CASE WHEN o.status <> 'cancelled' THEN i.quantity * i.unit_price ELSE 0 END) AS sales_amount
FROM authors a
LEFT JOIN books b ON b.author_id = a.author_id
LEFT JOIN order_items i ON i.book_id = b.book_id
LEFT JOIN orders o ON o.order_id = i.order_id
GROUP BY a.author_id;
