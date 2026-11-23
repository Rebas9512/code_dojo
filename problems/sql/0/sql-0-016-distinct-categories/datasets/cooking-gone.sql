DELETE FROM order_items WHERE book_id IN (SELECT book_id FROM books WHERE category = 'cooking');
DELETE FROM ratings WHERE book_id IN (SELECT book_id FROM books WHERE category = 'cooking');
DELETE FROM books WHERE category = 'cooking';
