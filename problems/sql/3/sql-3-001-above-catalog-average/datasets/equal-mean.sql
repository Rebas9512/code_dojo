UPDATE books SET price = CASE WHEN book_id = 1 THEN 30 WHEN book_id = 2 THEN 10 ELSE 20 END;
